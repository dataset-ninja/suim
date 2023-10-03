import supervisely as sly
import os
import numpy as np
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    batch_size = 30

    dataset_path = "/home/alex/DATASETS/TODO/Underwater Imagery (SUIM)/archive"
    images_folder = "images"
    masks_folder = "masks"
    images_ext = ".jpg"
    masks_ext = ".bmp"


    bad_data = [  # bad annotations, more 3000 different pixel values in ann...
        "f_r_1154_",
        "f_r_1664_",
        "w_r_136_",
        "f_r_1491_",
        "f_r_907_",
        "f_r_546_",
        "f_r_1133_",
        "f_r_968_",
        "f_r_991_",
        "f_r_940_",
        "d_r_135_",
        "f_r_647_",
        "f_r_1058_",
        "f_r_401_",
        "f_r_407_",
        "f_r_1324_",
        "d_r_759_",
        "f_r_1515_",
        "f_r_1424_",
        "f_r_797_",
        "f_r_499_",
        "d_r_293_",
        "f_r_829_",
        "f_r_1332_",
        "d_r_273_",
        "f_r_1812_",
        "d_r_20_",
        "w_r_7_",
        "d_r_270_",
        "w_r_47_",
        "d_r_301_",
        "d_r_65_",
        "f_r_500_",
        "d_r_564_",
        "d_r_5_",
        "f_r_43_",
        "f_r_1069_",
        "d_r_741_",
        "f_r_903_",
        "w_r_158_",
        "f_r_963_",
        "w_r_25_",
        "f_r_1142_",
        "f_r_1013_",
        "d_r_633_",
        "f_r_1006_",
        "f_r_1246_",
        "d_r_59_",
        "f_r_1879_",
        "f_r_936_",
        "d_r_174_",
        "f_r_1290_",
        "f_r_1259_",
        "d_r_473_",
        "d_r_470_",
        "f_r_1214_",
        "f_r_1151_",
        "f_r_921_",
        "f_r_1300_",
        "f_r_1007_",
        "f_r_1289_",
        "f_r_1274_",
        "d_r_310_",
        "d_r_189_",
        "w_r_1_",
        "d_r_179_",
        "f_r_1302_",
        "f_r_1382_",
        "f_r_934_",
        "f_r_1570_",
        "f_r_1183_",
        "f_r_1233_",
        "f_r_1816_",
        "w_r_24_",
        "f_r_1779_",
        "f_r_1394_",
        "f_r_1070_",
        "d_r_112_",
        "w_r_27_",
        "d_r_333_",
        "f_r_1068_",
        "f_r_1318_",
        "f_r_1267_",
        "f_r_1866_",
        "w_r_198_",
    ]


    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            # if col != 0:
            unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors


    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        image_name = get_file_name(image_path)
        mask_path = os.path.join(masks_path, image_name + masks_ext)

        mask_np = sly.imaging.image.read(mask_path)
        img_height1 = mask_np.shape[0]
        img_wight1 = mask_np.shape[1]
        if img_height != img_height1 or img_wight != img_wight1:
            return sly.Annotation(img_size=(img_height, img_wight), labels=labels)
        unique_colors = get_unique_colors(mask_np)
        for color in unique_colors:
            obj_class = color_to_class.get(color)
            mask = np.all(mask_np == color, axis=2)
            bitmap = sly.Bitmap(data=mask)
            label = sly.Label(bitmap, obj_class)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)


    obj_class_fish = sly.ObjClass("fish_and_vertebrates", sly.Bitmap, color=(255, 255, 0))
    obj_class_reefs = sly.ObjClass("reefs_and_invertebrates", sly.Bitmap, color=(255, 0, 255))
    obj_class_plants = sly.ObjClass("raquatic_plants", sly.Bitmap, color=(0, 255, 0))
    obj_class_ruins = sly.ObjClass("wrecks/ruins", sly.Bitmap, color=(0, 255, 255))
    obj_class_divers = sly.ObjClass("human_divers", sly.Bitmap, color=(0, 0, 255))
    obj_class_robots = sly.ObjClass("robots", sly.Bitmap, color=(255, 0, 0))
    obj_class_floor = sly.ObjClass("sea-floor", sly.Bitmap, color=(255, 255, 255))
    obj_class_back = sly.ObjClass("waterbody", sly.Bitmap, color=(0, 0, 0))

    color_to_class = {
        (255, 255, 0): obj_class_fish,
        (255, 0, 255): obj_class_reefs,
        (0, 255, 0): obj_class_plants,
        (0, 255, 255): obj_class_ruins,
        (0, 0, 255): obj_class_divers,
        (255, 0, 0): obj_class_robots,
        (255, 255, 255): obj_class_floor,
        (0, 0, 0): obj_class_back,
    }


    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(color_to_class.values()))
    api.project.update_meta(project.id, meta.to_json())

    for ds_name in os.listdir(dataset_path):
        dataset = api.dataset.create(project.id, ds_name.lower(), change_name_if_conflict=True)
        curr_ds_path = os.path.join(dataset_path, ds_name)
        images_path = os.path.join(curr_ds_path, images_folder)
        masks_path = os.path.join(curr_ds_path, masks_folder)

        if ds_name == "train_val":
            images_names = [
                im_name for im_name in os.listdir(images_path) if get_file_name(im_name) not in bad_data
            ]
        else:
            images_names = os.listdir(images_path)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))

    return project
