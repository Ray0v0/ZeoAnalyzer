import re
import os

class FeatureExtractor:
    def __init__(self, zeopp_command_generator, zeopp_file_analyzer):
        self.zeopp_command_generator = zeopp_command_generator
        self.zeopp_file_analyzer = zeopp_file_analyzer

    def generate_zeopp_command(self, cif_file, output_file_base):
        return self.zeopp_command_generator(cif_file, output_file_base)

    def analyse_zeopp_file(self, output_file_base):
        return self.zeopp_file_analyzer(output_file_base)

# 定义zeopp -res

def zeopp_res_command_generator(cif_file, output_file_base):
    return f"./network -res {output_file_base}.res {cif_file}"

def zeopp_res_file_analyzer(output_file_base):
    assert os.path.exists(output_file_base + '.res'), f"{output_file_base}.res doesn't exist!"

    with open(output_file_base + '.res', 'r') as f:
        output_text = f.read()

    feature_dict = {}
    outputs = output_text.split()
    feature_dict['maxIncDiam'] = float(outputs[1])
    feature_dict['maxDiam'] = float(outputs[2])
    feature_dict['incDiam'] = float(outputs[3])

    return feature_dict

zeopp_res = FeatureExtractor(zeopp_res_command_generator, zeopp_res_file_analyzer)

# 定义zeopp -sa

def zeopp_sa_command_generator(cif_file, output_file_base, chan_radius=0.45, probe_radius=0.45, num_samples=10000):
    return f"./network -sa {chan_radius} {probe_radius} {num_samples} {output_file_base}.sa {cif_file}"


def zeopp_sa_file_analyzer(output_file_base):
    assert os.path.exists(output_file_base + '.sa'), f"{output_file_base}.sa doesn't exist!"

    with open(output_file_base + '.sa', 'r') as f:
        output_text = f.read()

    feature_dict = {}

    volume_match = re.search(r"Unitcell_volume:\s*(\d+\.?\d*)", output_text)
    feature_dict['unitcell_volume'] = float(volume_match.group(1)) if volume_match else -1.0

    density_match = re.search(r"Density:\s*(\d+\.?\d*)", output_text)
    feature_dict['density'] = float(density_match.group(1)) if density_match else -1.0

    asa_a2_match = re.search(r"ASA_A\^2:\s*(\d+\.?\d*)", output_text)
    feature_dict['asa_a2'] = float(asa_a2_match.group(1)) if asa_a2_match else -1.0

    asa_m2_cm3_match = re.search(r"ASA_m\^2/cm\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['asa_m2_cm3'] = float(asa_m2_cm3_match.group(1)) if asa_m2_cm3_match else -1.0

    asa_m2_g_match = re.search(r"ASA_m\^2/g:\s*(\d+\.?\d*)", output_text)
    feature_dict['asa_m2_g'] = float(asa_m2_g_match.group(1)) if asa_m2_g_match else -1.0

    nasa_a2_match = re.search(r"NASA_A\^2:\s*(\d+\.?\d*)", output_text)
    feature_dict['nasa_a2'] = float(nasa_a2_match.group(1)) if nasa_a2_match else -1.0

    nav_a3_match = re.search(r"NAV_A\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['nav_a3'] = float(nav_a3_match.group(1)) if nav_a3_match else -1.0

    nasa_m2_cm3_match = re.search(r"NASA_m\^2/cm\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['nasa_m2_cm3'] = float(nasa_m2_cm3_match.group(1)) if nasa_m2_cm3_match else -1.0

    nasa_m2_g_match = re.search(r"NASA_m\^2/g:\s*(\d+\.?\d*)", output_text)
    feature_dict['nasa_m2_g'] = float(nasa_m2_g_match.group(1)) if nasa_m2_g_match else -1.0

    channels_match = re.search(r"Number_of_channels:\s*(\d+)", output_text)
    feature_dict['num_channels'] = int(channels_match.group(1)) if channels_match else -1.0

    channel_surface_area_match = re.search(r"Channel_surface_area_A\^2:\s*(\d+\.?\d*)", output_text)
    feature_dict['channel_surface_area'] = float(channel_surface_area_match.group(1)) if channel_surface_area_match else -1.0

    pockets_match = re.search(r"Number_of_pockets:\s*(\d+)", output_text)
    feature_dict['num_pockets'] = int(pockets_match.group(1)) if pockets_match else -1.0

    pocket_surface_area_match = re.search(r"Pocket_surface_area_A\^2:\s*(\d+\.?\d*)", output_text)
    feature_dict['pocket_surface_area'] = float(pocket_surface_area_match.group(1)) if pocket_surface_area_match else -1.0

    return feature_dict

zeopp_sa = FeatureExtractor(zeopp_sa_command_generator, zeopp_sa_file_analyzer)

# 定义zeopp -vol

def zeopp_vol_command_generator(cif_file, output_file_base, chan_radius=0.45, probe_radius=0.45, num_samples=10000):
    return f"./network -vol {chan_radius} {probe_radius} {num_samples} {output_file_base}.vol {cif_file}"

def zeopp_vol_file_analyzer(output_file_base):
    assert os.path.exists(output_file_base + '.vol'), f"{output_file_base}.vol doesn't exist!"

    with open(output_file_base + '.vol', 'r') as f:
        output_text = f.read()

    feature_dict = {}

    volume_match = re.search(r"Unitcell_volume:\s*(\d+\.?\d*)", output_text)
    feature_dict['unitcell_volume'] = float(volume_match.group(1)) if volume_match else -1

    density_match = re.search(r"Density:\s*(\d+\.?\d*)", output_text)
    feature_dict['density'] = float(density_match.group(1)) if density_match else -1

    av_a3_match = re.search(r"AV_A\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['av_a3'] = float(av_a3_match.group(1)) if av_a3_match else -1

    av_volume_fraction_match = re.search(r"AV_Volume_fraction:\s*(\d+\.?\d*)", output_text)
    feature_dict['av_volume_fraction'] = float(av_volume_fraction_match.group(1)) if av_volume_fraction_match else -1

    av_cm3_g_match = re.search(r"AV_cm\^3/g:\s*(\d+\.?\d*)", output_text)
    feature_dict['av_cm3_g'] = float(av_cm3_g_match.group(1)) if av_cm3_g_match else -1

    nav_a3_match = re.search(r"NAV_A\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['nav_a3'] = float(nav_a3_match.group(1)) if nav_a3_match else -1

    nav_volume_fraction_match = re.search(r"NAV_Volume_fraction:\s*(\d+\.?\d*)", output_text)
    feature_dict['nav_volume_fraction'] = float(nav_volume_fraction_match.group(1)) if nav_volume_fraction_match else -1

    nav_cm3_g_match = re.search(r"NAV_cm\^3/g:\s*(\d+\.?\d*)", output_text)
    feature_dict['nav_cm3_g'] = float(nav_cm3_g_match.group(1)) if nav_cm3_g_match else -1

    channels_match = re.search(r"Number_of_channels:\s*(\d+)", output_text)
    feature_dict['num_channels'] = int(channels_match.group(1)) if channels_match else -1

    channel_volume_match = re.search(r"Channel_volume_A\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['channel_volume'] = float(channel_volume_match.group(1)) if channel_volume_match else -1

    pockets_match = re.search(r"Number_of_pockets:\s*(\d+)", output_text)
    feature_dict['num_pockets'] = int(pockets_match.group(1)) if pockets_match else -1

    pocket_volume_match = re.search(r"Pocket_volume_A\^3:\s*(\d+\.?\d*)", output_text)
    feature_dict['pocket_volume'] = float(pocket_volume_match.group(1)) if pocket_volume_match else -1

    return feature_dict

zeopp_vol = FeatureExtractor(zeopp_vol_command_generator, zeopp_vol_file_analyzer)