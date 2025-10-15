#!/bin/bash

#SBATCH --gres=shard:1
#SBATCH -c 8
#SBATCH -w cl-siberiancat
#SBATCH -o /win/conger/user/ogura/RCCM/slurm/slurm-%j_inference.out

export PYTHONPATH=/win/conger/user/ogura/RCCM/MedicalDataAugmentationTool-VerSe:\
/win/conger/user/ogura/RCCM/MedicalDataAugmentationTool-VerSe/MedicalDataAugmentationTool:$PYTHONPATH



singularity exec --nv \
  -B /data03/user:/data03/user,/win/conger/user:/win/conger/user,/win/salmon/user:/win/salmon/user \
  /win/salmon/user/ogura/singularity_images/verse2020/verse2020.sif \
  python3 /win/conger/user/ogura/RCCM/MedicalDataAugmentationTool-VerSe/verse2020/inference/run_inference.py \
  --image_folder /data03/user/ogura/Uzumasa \
  --output_folder /win/conger/user/ogura/Uzumasa/results \
  --input_ext .mhd \
  --delete_tmp