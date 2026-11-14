"""Mid.0 stability sweep, based on the existing biased sweep; saves perturbation norms."""

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

import numpy as np
from PIL import Image


FEATURE = None
FACTORS = [-120, -100, -75, -50, -30, -20, -15, -10, -7, -5, -3, 0, 3, 5, 7, 10, 15, 20, 30, 50, 75, 100, 120]
DEFAULT_BLOCK = "unet.mid_block.attentions.0"
DEFAULT_GROUPS = [
    "black_man", "black_woman", "white_man", "white_woman",
    "east_asian_man", "east_asian_woman", "middle_eastern_man", "middle_eastern_woman",
    "indian_man", "indian_woman", "hispanic_man", "hispanic_woman",
]


def find_project_root():
    explicit = os.environ.get("SAE_PROJECT_ROOT")
    if explicit:
        return Path(explicit).expanduser().resolve()
    for start in (Path(__file__).resolve(), Path.cwd()):
        for parent in (start, *start.parents):
            if (parent / "data/datasets/biased/images").is_dir() and (parent / "sdxl-unbox").is_dir():
                return parent
    raise FileNotFoundError("Set SAE_PROJECT_ROOT to the workspace containing data/datasets/biased and sdxl-unbox.")


def slug(value):
    value = int(value)
    return f"m{abs(value)}" if value < 0 else f"p{value}"


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    global FEATURE, FACTORS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature", type=int, required=True, help="SAE dictionary feature index (0–5119)")
    parser.add_argument("--groups", nargs="+", default=DEFAULT_GROUPS,
                        help="biased dataset image groups, e.g. middle_eastern_woman")
    parser.add_argument("--samples-per-group", type=int, default=20,
                        help="number of consecutive seeds to use in each group after sorting by original seed")
    parser.add_argument("--seed-start", type=int, default=0,
                        help="zero-based offset into each group's sorted biased-dataset seeds")
    parser.add_argument("--face-boxes", default=None,
                        help="CSV of automatic boxes with sample_id/source/label/x1/y1/x2/y2 columns")
    parser.add_argument("--mask-intervention-to-face-box", action="store_true",
                        help="apply the SAE edit only to activation cells inside the automatic human-face box")
    parser.add_argument("--face-region", choices=("full", "upper", "middle", "lower"), default="full",
                        help="when face masking, restrict to a vertical third of the automatic face box")
    parser.add_argument("--block", default=DEFAULT_BLOCK,
                        help="U-Net block with a matching pretrained SAE checkpoint")
    parser.add_argument("--checkpoint", default=None,
                        help="SAE checkpoint directory; defaults to the matching standard checkpoint")
    parser.add_argument("--alphas", nargs="+", type=int, default=FACTORS,
                        help="integer feature multipliers; must include 1 for the unedited control")
    parser.add_argument("--output", default=None,
                        help="output directory, relative to the project root unless absolute")
    parser.add_argument("--reuse-images-from", nargs="*", type=Path, default=[], help="Prior run roots with matching reuse_provenance.json")
    args = parser.parse_args()
    if args.block != "unet.mid_block.attentions.0":
        parser.error("This stability runner is restricted to mid.0")
    FEATURE = args.feature
    FACTORS = [1] + [a for a in args.alphas if a != 1]
    if not 0 <= FEATURE < 5120:
        parser.error("--feature must be between 0 and 5119")
    if 1 not in FACTORS:
        parser.error("--alphas must include 1 for the unedited control")
    if args.mask_intervention_to_face_box and not args.face_boxes:
        parser.error("--mask-intervention-to-face-box requires --face-boxes")
    if args.face_region != "full" and not args.mask_intervention_to_face_box:
        parser.error("--face-region requires --mask-intervention-to-face-box")
    if args.output is None:
        args.output = f"sae-activation-tuning/tuning_activations/feature_{FEATURE}/run_biased_slurm"
    root = find_project_root()
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {output}")

    manifest_path = root / "backprop/manifest.csv"
    dataset_root = root / "data/datasets/biased/images"
    with manifest_path.open(newline="") as f:
        manifest = list(csv.DictReader(f))
    expected_groups = {f"{r}_{g}" for r in ("black", "white", "east_asian", "middle_eastern", "indian", "hispanic")
                       for g in ("man", "woman")}
    if not set(args.groups) <= expected_groups:
        raise ValueError(f"Unknown groups: {sorted(set(args.groups) - expected_groups)}")
    rows_by_group = {}
    for group in args.groups:
        rows = [r for r in manifest if f"{r['race_prompt'].replace(' ', '_')}_{r['gender_prompt']}" == group]
        rows.sort(key=lambda r: int(r["seed"]))
        if len(rows) != 100 or any(r["prompt"] != f"a picture of a {r['race_prompt']} {r['gender_prompt']}" for r in rows):
            raise ValueError(f"Expected the 100-image simple-prompt biased group in {group}; got {len(rows)} rows")
        rows = rows[args.seed_start:args.seed_start + args.samples_per_group]
        if len(rows) != args.samples_per_group:
            raise ValueError(f"Expected {args.samples_per_group} images in group {group}; got {len(rows)}")
        for r in rows:
            source = dataset_root / Path(r["image"]).relative_to("images")
            if not source.is_file():
                raise FileNotFoundError(source)
        rows_by_group[group] = rows

    face_box_by_sample = {}
    if args.mask_intervention_to_face_box:
        with Path(args.face_boxes).expanduser().open(newline="") as f:
            for item in csv.DictReader(f):
                if item["source"] != "objects" or item["label"].strip().lower() != "human face":
                    continue
                box = tuple(float(item[key]) / 512.0 for key in ("x1", "y1", "x2", "y2"))
                if box[2] <= box[0] or box[3] <= box[1]:
                    continue
                old = face_box_by_sample.get(item["sample_id"])
                if old is None or (box[2] - box[0]) * (box[3] - box[1]) > (old[2] - old[0]) * (old[3] - old[1]):
                    face_box_by_sample[item["sample_id"]] = box
        required = {f"{group}_seed{int(row['seed']):03d}" for group, rows in rows_by_group.items() for row in rows}
        missing = sorted(required - set(face_box_by_sample))
        if missing:
            raise ValueError(f"Missing automatic human-face boxes for {len(missing)} samples, e.g. {missing[:3]}")

    (output / "images").mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(root / "sdxl-unbox"))
    import torch
    from diffusers import AutoencoderKL, EulerAncestralDiscreteScheduler
    from SDLens import HookedStableDiffusionXLPipeline
    from SAE import SparseAutoencoder

    settings_in = json.loads((root / "backprop/generation_settings.json").read_text())
    checkpoint = Path(args.checkpoint).expanduser() if args.checkpoint else (
        root / "sdxl-unbox/checkpoints" /
        f"{args.block}_k10_hidden5120_auxk256_bs4096_lr0.0001/final"
    )
    if not checkpoint.is_absolute():
        checkpoint = root / checkpoint
    checkpoint = checkpoint.resolve()
    if not (checkpoint / "state_dict.pth").is_file():
        raise FileNotFoundError(f"Missing SAE checkpoint weights: {checkpoint / 'state_dict.pth'}")
    torch.set_num_threads(4)
    load = dict(torch_dtype=torch.float16, cache_dir=str(root / "ReNO/hf_cache"), local_files_only=True)
    vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", **load)
    pipe = HookedStableDiffusionXLPipeline.from_pretrained(
        "stabilityai/sdxl-turbo", vae=vae, variant="fp16", **load
    )
    pipe.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
        pipe.pipe.scheduler.config, timestep_spacing="trailing"
    )
    pipe.pipe.to("cuda")
    pipe.pipe.set_progress_bar_config(disable=True)
    sae = SparseAutoencoder.load_from_disk(str(checkpoint)).float().cuda().eval()
    sae.requires_grad_(False)
    reusable = []
    import importlib.metadata as metadata
    for reuse_root in args.reuse_images_from:
        provenance = json.loads((reuse_root / "reuse_provenance.json").read_text())
        if provenance["checkpoint_sha256"] != sha256(checkpoint / "state_dict.pth") or provenance["block"] != args.block:
            raise ValueError("Reuse checkpoint/layer mismatch")
        if any(provenance["software_versions"][name] != metadata.version(name) for name in ("torch", "diffusers", "transformers")):
            raise ValueError("Reuse software version mismatch")
        reusable.append(reuse_root / f"feature_{FEATURE}")

    def hook_for(alpha, captured, face_box=None):
        @torch.no_grad()
        def hook(module, inputs, output):
            original = output[0]
            residual = (original - inputs[0]).permute(0, 2, 3, 1).float()
            codes = sae.encode(residual)
            coefficient = codes[..., FEATURE:FEATURE + 1]
            change = coefficient * (alpha - 1.0)
            if face_box is not None:
                x1, y1, x2, y2 = face_box
                third = (y2 - y1) / 3.0
                if args.face_region == "upper":
                    y2 = y1 + third
                elif args.face_region == "middle":
                    y1, y2 = y1 + third, y1 + 2 * third
                elif args.face_region == "lower":
                    y1 = y1 + 2 * third
                h, w = coefficient.shape[1:3]
                xs = (torch.arange(w, device=coefficient.device, dtype=coefficient.dtype) + 0.5) / w
                ys = (torch.arange(h, device=coefficient.device, dtype=coefficient.dtype) + 0.5) / h
                mask = ((ys[:, None] >= y1) & (ys[:, None] <= y2) &
                        (xs[None, :] >= x1) & (xs[None, :] <= x2)).to(coefficient.dtype)
                change = change * mask[None, ..., None]
            delta = change @ sae.decoder.weight[:, FEATURE:FEATURE + 1].T
            edited = original + delta.permute(0, 3, 1, 2).to(original)
            post = sae.encode((edited - inputs[0]).permute(0, 2, 3, 1).float())
            if not torch.isfinite(edited).all() or not torch.isfinite(post).all():
                raise FloatingPointError(f"Non-finite activations at alpha {alpha}")
            captured.update(
                original_block_fro=float(original.float().norm().item()),
                original_residual_fro=float(residual.norm().item()),
                delta_fro_precast=float(delta.norm().item()),
                delta_fro_applied=float((edited.float()-original.float()).norm().item()),
                decoder_norm=float(sae.decoder.weight[:, FEATURE].norm().item()),
                pre=coefficient[0, ..., 0].float().cpu().numpy(),
                post=post[0, ..., FEATURE].float().cpu().numpy(),
                scaled=(coefficient[0, ..., 0] * alpha).float().cpu().numpy(),
                change_map=change[0, ..., 0].float().cpu().numpy(),
                pre_mean=float(coefficient.mean().item()),
                scaled_mean=float((coefficient * alpha).mean().item()),
                scaled_abs_mean=float((coefficient * alpha).abs().mean().item()),
                change_mean=float(change.abs().mean().item()),
                post_mean=float(post[..., FEATURE].mean().item()),
                active_fraction=float((post[..., FEATURE] > 0).float().mean().item()),
            )
            if alpha == 1:
                captured["_reference"] = (inputs, output)
            return (edited,) + output[1:]
        return hook

    map_keys, pre_maps, post_maps, scaled_maps, footprint_maps = [], [], [], [], []
    metric_rows, review_rows = [], []
    for group in args.groups:
        group_maps = {k: [] for k in ("pre", "post", "scaled", "footprint")}
        for row in rows_by_group[group]:
            seed = int(row["seed"])
            source = dataset_root / Path(row["image"]).relative_to("images")
            baseline = output / "images" / group / "baseline" / f"seed{seed:03d}.png"
            baseline.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, baseline)
            base_rgb = np.asarray(Image.open(source).convert("RGB"), dtype=np.float32)
            key_pre = None
            face_box = face_box_by_sample.get(f"{group}_seed{seed:03d}")
            reference = None
            verified_reuse = set()
            for alpha in FACTORS:
                captured = {}
                # Match the source dataset's independent CUDA generators for noise and scheduler.
                noise_rng = torch.Generator("cuda").manual_seed(seed)
                scheduler_rng = torch.Generator("cuda").manual_seed(seed)
                latents = torch.randn((1, 4, 64, 64), generator=noise_rng, device="cuda", dtype=torch.float16)
                reuse_path = next((r / "images" / group / f"seed{seed:03d}_alpha_{slug(alpha)}.png"
                                   for r in reusable if (r / "images" / group / f"seed{seed:03d}_alpha_{slug(alpha)}.png").exists()), None)
                reused = reuse_path is not None and alpha != 1 and any(reuse_path.is_relative_to(r) for r in verified_reuse)
                if reused:
                    if reference is None or settings_in["steps"] != 1:
                        raise ValueError("Reuse requires a captured single-step alpha=1 reference")
                    hook_for(alpha, captured, face_box)(None, reference[0], reference[1])
                    image = Image.open(reuse_path).convert("RGB")
                else:
                    result = pipe.run_with_hooks(
                        prompt=row["prompt"], latents=latents, generator=scheduler_rng,
                        num_inference_steps=settings_in["steps"], guidance_scale=settings_in["guidance_scale"],
                        height=settings_in["height"], width=settings_in["width"],
                        position_hook_dict={args.block: hook_for(alpha, captured, face_box)},
                    )
                    image = result.images[0].convert("RGB")
                if alpha == 1:
                    reference = captured.pop("_reference")
                    for reuse_dir in reusable:
                        prior = reuse_dir / "images" / group / f"seed{seed:03d}_alpha_p1.png"
                        if prior.exists() and np.array_equal(np.array(image), np.array(Image.open(prior).convert("RGB"))):
                            verified_reuse.add(reuse_dir)
                image_path = output / "images" / group / f"seed{seed:03d}_alpha_{slug(alpha)}.png"
                image.save(image_path)
                mae = float(np.abs(np.asarray(image, dtype=np.float32) - base_rgb).mean())
                if key_pre is None:
                    key_pre = captured["pre"]
                group_maps["post"].append(captured["post"])
                group_maps["scaled"].append(captured["scaled"])
                group_maps["footprint"].append(np.abs(captured["change_map"]))
                metric_rows.append({
                    "group": group, "seed": seed, "feature": FEATURE, "alpha": alpha,
                    "prompt": row["prompt"], "source_image": str(source.relative_to(root)),
                    "pre_mean_activation": captured["pre_mean"],
                    "mean_scaled_coefficient": captured["scaled_mean"],
                    "mean_abs_scaled_coefficient": captured["scaled_abs_mean"],
                    "mean_abs_intervention_coefficient_change": captured["change_mean"],
                    "post_reencoded_mean_activation": captured["post_mean"],
                    "post_reencoded_active_fraction": captured["active_fraction"],
                    "pixel_mae_vs_original": mae,
                    "reused_image": reused,
                    "reuse_source": str(reuse_path) if reused else "",
                    "original_block_fro": captured["original_block_fro"],
                    "original_residual_fro": captured["original_residual_fro"],
                    "delta_fro_precast": captured["delta_fro_precast"],
                    "delta_fro_applied": captured["delta_fro_applied"],
                    "relative_delta_block_fro": captured["delta_fro_applied"] / max(captured["original_block_fro"], 1e-12),
                    "relative_delta_residual_fro": captured["delta_fro_applied"] / max(captured["original_residual_fro"], 1e-12),
                    "decoder_norm": captured["decoder_norm"],
                })
                review_rows.append({
                    "group": group, "seed": seed, "feature": FEATURE, "alpha": alpha,
                    "source_image": str(source.relative_to(root)), "visible_attribute_notes": "",
                    "face_or_hair_damage": "", "other_artifacts": "", "notes": "",
                })
            group_maps["pre"].append(key_pre)
            map_keys.append(f"{group}|{seed}")
            print(f"Completed {group} seed={seed}; {len(metric_rows)} alpha results", flush=True)
        pre_maps.extend(group_maps["pre"])
        post_maps.extend(np.asarray(group_maps["post"]).reshape(len(rows_by_group[group]), len(FACTORS), *group_maps["post"][0].shape))
        scaled_maps.extend(np.asarray(group_maps["scaled"]).reshape(len(rows_by_group[group]), len(FACTORS), *group_maps["scaled"][0].shape))
        footprint_maps.extend(np.asarray(group_maps["footprint"]).reshape(len(rows_by_group[group]), len(FACTORS), *group_maps["footprint"][0].shape))

    metric_rows.sort(key=lambda r: (args.groups.index(r["group"]), int(r["seed"]), int(r["alpha"])))
    review_rows.sort(key=lambda r: (args.groups.index(r["group"]), int(r["seed"]), int(r["alpha"])))
    write_csv(output / "metrics.csv", metric_rows)
    write_csv(output / "visual_review.csv", review_rows)
    np.savez_compressed(
        output / "activation_maps.npz",
        pre_maps=np.asarray(pre_maps, dtype=np.float32),
        post_reencoded_maps=np.asarray(post_maps, dtype=np.float32),
        intervention_footprint_maps=np.asarray(footprint_maps, dtype=np.float32),
        scaled_coefficient_maps=np.asarray(scaled_maps, dtype=np.float32),
        map_keys=np.asarray(map_keys), multipliers=np.asarray(FACTORS),
    )
    settings_out = {
        "software_versions": {name: __import__("importlib.metadata", fromlist=["version"]).version(name) for name in ("torch", "diffusers", "transformers", "numpy")},
        "runner": "layers/mid0_stability/generate_sweep.py",
        "reuse_images_from": [str(r) for r in args.reuse_images_from],
        "feature": FEATURE,
        "source_dataset": "data/datasets/biased (simple-prompt set)",
        "source_manifest": "backprop/manifest.csv",
        "groups": args.groups,
        "samples_per_group": args.samples_per_group,
        "seed_start": args.seed_start,
        "face_box_mask": bool(args.mask_intervention_to_face_box),
        "face_region": args.face_region,
        "face_box_source": str(Path(args.face_boxes).expanduser()) if args.face_boxes else None,
        "prompt_template": settings_in["prompt_template"],
        "alphas": FACTORS,
        "intervention": ("block output plus (alpha - 1) times the original SAE coefficient times its decoder direction; alpha +1 is the no-op"
                         + ("; edit is spatially restricted to automatic human-face-box cells" if args.mask_intervention_to_face_box else "")),
        "block": args.block,
        "checkpoint": str(checkpoint.relative_to(root)),
        "model": settings_in["model"], "vae": settings_in["vae"],
        "steps": settings_in["steps"], "guidance_scale": settings_in["guidance_scale"],
        "height": settings_in["height"], "width": settings_in["width"],
        "scheduler": settings_in["scheduler"], "timestep_spacing": settings_in["timestep_spacing"],
        "seed_replay": "The original biased-dataset seed and prompt are replayed for each alpha; original dataset PNG is retained for the original tile and pixel MAE reference.",
        "sae_weights_sha256": sha256(checkpoint / "state_dict.pth"),
        "run": output.name,
    }
    (output / "settings.json").write_text(json.dumps(settings_out, indent=2) + "\n")
    print(f"Saved {len(metric_rows)} alpha results in {output}; now run render_signed_visuals.py", flush=True)


if __name__ == "__main__":
    main()
