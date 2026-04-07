# Morris Worm Attack Lab (SEED Labs)

This repo contains my work for the **SEED Labs – Morris Worm Attack** assignment. The lab describes and implement how a classic Internet worm can:
1) exploit a buffer overflow for remote code execution, and
2) self-duplicate + propagate across an emulated “mini Internet” running in Docker.

## What’s in this repo
- `MorrisWorm_Lab_Report.pdf`  — polished lab report (task-by-task, with observations and takeaways)
- `worm.py` — my modified worm implementation (based on the provided skeleton)
- `MorrisWorm_Attack_Lab.pdf` — official lab instructions (SEED Labs)


## Environment

- Ubuntu 20.04 (SEED VM recommended)
- Docker + Docker Compose

The lab includes two emulated Internets:
- **internet-nano** (smaller, faster) for most tasks
- **internet-mini** (larger) for the final release/propagation task

## Quick start

1. Unzip the lab setup folder provided by SEED Labs.
2. Start the emulator (nano):
   ```bash
   cd Labsetup/internet-nano
   dcbuild
   dcup
   ```
3. Start the map (if your Labsetup has it as a separate folder):
   ```bash
   cd Labsetup/map
   dcbuild
   dcup
   ```
4. Open the map:
   - http://localhost:8080/map.html

## Running the worm (lab containers only)

Inside the attacker container:
```bash
chmod +x worm.py
./worm.py
```

> This worm expects the vulnerable server from the lab to be running on port `9090` on target hosts.

## Notes

- In my setup, the map container wasn’t present as a separate `Labsetup/map` folder. The map UI was still reachable at:
  - `http://localhost:8080/map.html`
  This appears to be a packaging difference across lab versions.

## References

- SEED Labs — Morris Worm Attack Lab (Wenliang Du).
