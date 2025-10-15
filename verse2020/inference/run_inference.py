import os
import argparse
import subprocess
import shutil

def main(args):
    
    # preprocess
    preprocess_script = os.path.join(os.path.dirname(__file__), '../other/preprocess.py')
    tmp_preprocess_dir = os.path.join(args.output_folder, 'tmp_preprocess')
    os.makedirs(tmp_preprocess_dir, exist_ok=True)
    preprocess_cmd = [
        'python', preprocess_script,
        '--image_folder', args.image_folder,
        '--output_folder', tmp_preprocess_dir,
        '--sigma', "0.75",
        '--input_ext', args.input_ext
    ]
    subprocess.run(preprocess_cmd)
    
    # spine localization
    spine_localization_script = os.path.join(os.path.dirname(__file__), 'main_spine_localization.py')
    tmp_spine_localization_dir = os.path.join(args.output_folder, 'spine_localization')
    os.makedirs(tmp_spine_localization_dir, exist_ok=True)
    spine_localization_cmd = [
        'python', spine_localization_script,
        '--image_folder', tmp_preprocess_dir,
        '--setup_folder', args.output_folder,
        '--model_files', os.path.join(os.path.dirname(__file__), '../models/spine_localization'),
        '--output_folder', tmp_spine_localization_dir
    ]
    subprocess.run(spine_localization_cmd)
    
    # vertebrae localization
    vertebrae_localization_script = os.path.join(os.path.dirname(__file__), 'main_vertebrae_localization.py')
    tmp_vertebrae_localization_dir = os.path.join(args.output_folder, 'vertebrae_localization')
    os.makedirs(tmp_vertebrae_localization_dir, exist_ok=True)
    vertebrae_localization_cmd = [
        'python', vertebrae_localization_script,
        '--image_folder', tmp_preprocess_dir,
        '--setup_folder', args.output_folder,
        '--model_files', os.path.join(os.path.dirname(__file__), '../models/vertebrae_localization'),
        '--output_folder', tmp_vertebrae_localization_dir
    ]
    subprocess.run(vertebrae_localization_cmd)
    
    # vertebrae segmentation
    vertebrae_segmentation_script = os.path.join(os.path.dirname(__file__), 'main_vertebrae_segmentation.py')
    vertebrae_segmentation_cmd = [
        'python', vertebrae_segmentation_script,
        '--image_folder', tmp_preprocess_dir,
        '--setup_folder', args.output_folder,
        '--model_files', os.path.join(os.path.dirname(__file__), '../models/vertebrae_segmentation'),
        '--output_folder', args.output_folder,
    ]
    subprocess.run(vertebrae_segmentation_cmd)
    
    if args.delete_tmp:
        shutil.rmtree(tmp_preprocess_dir, ignore_errors=False)
        shutil.rmtree(tmp_spine_localization_dir, ignore_errors=False)
        shutil.rmtree(tmp_vertebrae_localization_dir, ignore_errors=False)
        shutil.rmtree(os.path.join(args.output_folder, "output"), ignore_errors=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference for medical data augmentation.")
    parser.add_argument('--image_folder', type=str, required=True, help='Path to the folder containing input images.')
    parser.add_argument('--output_folder', type=str, required=True, help='Directory to save the output results.')
    parser.add_argument("--input_ext", type=str, default=".nii.gz", help="Input image extension")
    parser.add_argument('--delete_tmp', action='store_true', help='Whether to delete temporary files after processing.')
    
    args = parser.parse_args()
    
    main(args)