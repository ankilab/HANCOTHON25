"""
The following is a simple example algorithm.

It is meant to run within a container.

To run the container locally, you can call the following bash script:

  ./do_test_run.sh

This will start the inference and reads from ./test/input and writes to ./test/output

To save the container and prep it for upload to Grand-Challenge.org you can call:

  ./do_save.sh

Any container that shows the same behaviour will do, this is purely an example of how one COULD do it.

Reference the documentation to get details on the runtime environment on the platform:
https://grand-challenge.org/documentation/runtime-environment/

Happy programming!
"""

# ===========================================================================
# Imports
# ===========================================================================
from pathlib import Path
import json
from glob import glob
import SimpleITK
import random


# ===========================================================================
# Global Variables
# ===========================================================================
BASE_DIR = Path("inference.py").resolve().parent
if BASE_DIR == Path("/opt/app"):
    INPUT_PATH = Path("/input")
    OUTPUT_PATH = Path("/output")
    RESOURCE_PATH = Path("resources")
else:
    # The INPUT_PATH is added during the docker run
    # in the do_test_run.sh script with the "interf0" directory
    # We will therefore use this here as well.
    INPUT_PATH = BASE_DIR / "test" / "input" / "interf0"
    OUTPUT_PATH = BASE_DIR / "test" / "output" / "interf0"
    RESOURCE_PATH = BASE_DIR / "resources"

PREDICTION_TARGET_SLUG = "2-year-recurrence-after-diagnosis"
# PREDICTION_TARGET_SLUG = "5-year-survival"
random.seed(42)


# ===========================================================================
# Default Execution Methods
# ===========================================================================
def run():
    # The key is a tuple of the slugs of the input sockets
    interface_key = get_interface_key()

    # Lookup the handler for this particular set of sockets (i.e. the interface)
    handler = {
        (
            "hancock-blood-data",
            "hancock-clinical-data",
            "hancock-lymph-node-wsi-embeddings",
            "hancock-pathological-data",
            "hancock-primary-tumor-wsi-embeddings",
            "hancock-surgery-text-data",
            "hancock-tma-tumor-center-core-cd163-1",
            "hancock-tma-tumor-center-core-cd163-2",
            "hancock-tma-tumor-center-core-cd3-1",
            "hancock-tma-tumor-center-core-cd3-2",
            "hancock-tma-tumor-center-core-cd56-1",
            "hancock-tma-tumor-center-core-cd56-2",
            "hancock-tma-tumor-center-core-cd68-1",
            "hancock-tma-tumor-center-core-cd68-2",
            "hancock-tma-tumor-center-core-cd8-1",
            "hancock-tma-tumor-center-core-cd8-2",
            "hancock-tma-tumor-center-core-he-1",
            "hancock-tma-tumor-center-core-he-2",
            "hancock-tma-tumor-center-core-mhc-1-1",
            "hancock-tma-tumor-center-core-mhc-1-2",
            "hancock-tma-tumor-center-core-pd-l1-1",
            "hancock-tma-tumor-center-core-pd-l1-2",
        ): interf0_handler,
    }[interface_key]

    # Call the handler
    return handler()


def interf0_handler():
    # Read the input
    input_hancock_blood_data = load_json_file(
        location=INPUT_PATH / "hancock-blood-data.json",
    )
    input_hancock_clinical_data = load_json_file(
        location=INPUT_PATH / "hancock-clinical-data.json",
    )
    input_hancock_pathological_data = load_json_file(
        location=INPUT_PATH / "hancock-pathological-data.json",
    )
    input_hancock_primary_tumor_wsi_embeddings = load_json_file(
        location=INPUT_PATH / "hancock-primary-tumor-wsi-embeddings.json",
    )
    input_hancock_lymph_node_wsi_embeddings = load_json_file(
        location=INPUT_PATH / "hancock-lymph-node-wsi-embeddings.json",
    )
    input_hancock_tma_tumor_center_core_he_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_HE_1",
    )
    input_hancock_tma_tumor_center_core_he_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_HE_2",
    )
    input_hancock_tma_tumor_center_core_cd3_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD3_1",
    )
    input_hancock_tma_tumor_center_core_cd3_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD3_2",
    )
    input_hancock_tma_tumor_center_core_cd8_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD8_1",
    )
    input_hancock_tma_tumor_center_core_cd8_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD8_2",
    )
    input_hancock_tma_tumor_center_core_cd56_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD56_1",
    )
    input_hancock_tma_tumor_center_core_cd56_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD56_2",
    )
    input_hancock_tma_tumor_center_core_cd68_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD68_1",
    )
    input_hancock_tma_tumor_center_core_cd68_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD68_2",
    )
    input_hancock_tma_tumor_center_core_cd163_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD163_1",
    )
    input_hancock_tma_tumor_center_core_cd163_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_CD163_2",
    )
    input_hancock_tma_tumor_center_core_mhc_1_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_MHC-1_1",
    )
    input_hancock_tma_tumor_center_core_mhc_1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_MHC-1_2",
    )
    input_hancock_tma_tumor_center_core_pd_l1_1 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_PD-L1_1",
    )
    input_hancock_tma_tumor_center_core_pd_l1_2 = load_image_file_as_array(
        location=INPUT_PATH / "images/hancock_tma_tumor_center_PD-L1_2",
    )
    input_hancock_surgery_text_data = load_json_file(
        location=INPUT_PATH / "hancock-surgery-text-data.json",
    )

    # Check if a cudo device is available
    _show_torch_cuda_info()
    # Some additional resources might be required
    # Read some resource files
    with open(RESOURCE_PATH / "some_resource.txt", "r") as f:
        print(f.read())

    # Random prediction
    prediction = 1.0
    # ToDo: Implement your algorithm here

    # Convert the predicton to a string representation
    prediction_str = prediction_to_string(
        prediction=prediction, threshold=0.5, target_slug=PREDICTION_TARGET_SLUG
    )

    print(f"Your prediction is: {prediction_str}")

    # Save your output
    write_json_file(
        location=OUTPUT_PATH / get_output_file_name(PREDICTION_TARGET_SLUG),
        content=prediction_str,
    )

    return 0


def get_output_file_name(prediction_target_slug: str) -> str:
    """
    Returns the output file name based on the prediction target slug.

    Args:
        prediction_target_slug (str): The slug of the prediction target.

    Returns:
        str: The output file name.

    Raises:
        ValueError: If the prediction target slug is unknown.
    """
    if prediction_target_slug == "2-year-recurrence-after-diagnosis":
        return "2-year-recurrence.json"
    elif prediction_target_slug == "5-year-survival":
        return "5-year-survival.json"
    else:
        raise ValueError(
            f"Unknown prediction target slug: {prediction_target_slug}. "
            "Expected '2-year-recurrence-after-diagnosis' or '5-year-survival'."
        )


def get_interface_key():
    # The inputs.json is a system generated file that contains information about
    # the inputs that interface with the algorithm
    inputs = load_json_file(
        location=INPUT_PATH / "inputs.json",
    )
    socket_slugs = [sv["interface"]["slug"] for sv in inputs]
    return tuple(sorted(socket_slugs))


def load_json_file(*, location):
    # Reads a json file
    with open(location, "r") as f:
        return json.loads(f.read())


def write_json_file(*, location, content):
    location_path = Path(location)
    location_path.parent.mkdir(parents=True, exist_ok=True)
    # Writes a json file
    with open(location, "w") as f:
        f.write(json.dumps(content, indent=4))


def load_image_file_as_array(*, location):
    # Use SimpleITK to read a file
    input_files = (
        glob(str(location / "*.tif"))
        + glob(str(location / "*.tiff"))
        + glob(str(location / "*.mha"))
    )
    result = SimpleITK.ReadImage(input_files[0])

    # Convert it to a Numpy array
    return SimpleITK.GetArrayFromImage(result)


def _show_torch_cuda_info():
    import torch

    print("=+=" * 10)
    print("Collecting Torch CUDA information")
    print(f"Torch CUDA is available: {(available := torch.cuda.is_available())}")
    if available:
        print(f"\tnumber of devices: {torch.cuda.device_count()}")
        print(f"\tcurrent device: {(current_device := torch.cuda.current_device())}")
        print(f"\tproperties: {torch.cuda.get_device_properties(current_device)}")
    print("=+=" * 10, end='\n\n')


def survival_prediction_to_string(prediction: float, threshold: float = 0.5) -> str:
    """
    Converts a survival prediction to a string representation.

    Args:
        - prediction (float): The survival prediction value.
        - threshold (float): The threshold to determine the survival status. Greater
        than the threshold indicates death, less than or equal to the threshold indicates survival.
    """
    if prediction > threshold:
        return "deceased"
    else:
        return "living"


def recurrence_prediction_to_string(prediction: float, threshold: float = 0.5) -> str:
    """
    Converts a recurrence prediction to a string representation.

    Args:
        - prediction (float): The recurrence prediction value.
        - threshold (float): The threshold to determine the recurrence status. Greater
        than the threshold indicates recurrence, less than or equal to the threshold indicates no recurrence.
    """
    if prediction > threshold:
        return "recurrence"
    else:
        return "no recurrence"


def prediction_to_string(
    prediction: float,
    threshold: float = 0.5,
    target_slug: str = "2-year-recurrence-after-diagnosis",
) -> str:
    """
    Converts a prediction to a string representation based on the target slug.

    Args:
        - prediction (float): The prediction value.
        - threshold (float): The threshold to determine the status.
        - target_slug (str): The target slug to determine the type of prediction.
    """
    if target_slug == "2-year-recurrence-after-diagnosis":
        return recurrence_prediction_to_string(prediction, threshold)
    elif target_slug == "5-year-survival":
        return survival_prediction_to_string(prediction, threshold)
    else:
        raise ValueError(f"Unknown target slug: {target_slug}")


if __name__ == "__main__":
    raise SystemExit(run())
