import subprocess, os, shutil, glob
# Example usage
target_size_mb = 7
speed_multiply = 1
image_fps = 20
max_width_limit = 0.50
min_width_limit = 0.25  # 从25%宽度到50%

# target_size_mb = 5
# speed_multiply = 2
# image_fps = 10
# max_width_limit = 1.0
# min_width_limit = 0.5  # 从50%宽度到100%
# to_do_list = glob.glob("../*crop.mp4")

tmp_path = "G:/temp"
to_do_list = glob.glob("../*crop.mp4")

def bi_search(fn, range):    
    # 输入 fn 是一个递增过零点的函数
    # 输入 range 是一个fn的list
    # 返回 range 中的零点或零点左侧的值
    range = list(range)
    L, R = 0, len(range)-1
    y = fn(range[R])
    if y <= 0:
        return range[R]

    while (R-L>1):
        M = (L + R)//2
        y = fn(range[M])
        if y > 0:
            R = M
        elif y == 0: 
            return M
        else:
            L = M
        print(L, R)
    return range[L]



def create_gif(output_file, file, fps=20, fast_forward=1, fast=False, extra=False,
               quality=90, motion_quality=None, lossy_quality=None, width=None, height=None,
               sort=True, repeat=None, quiet=False):
    # Build command string
    command = ["gifski"]

    # Options
    command.append(f"-o {output_file}")

    # Flags
    command.append(f"-r {fps}")
    command.append(f"--fast-forward {fast_forward}")
    if fast:
        command.append("--fast")
    if extra:
        command.append("--extra")
    command.append(f"-Q {quality}")
    if motion_quality is not None:
        command.append(f"--motion-quality {motion_quality}")
    if lossy_quality is not None:
        command.append(f"--lossy-quality {lossy_quality}")
    if width is not None:
        command.append(f"-W {width}")
    if height is not None:
        command.append(f"-H {height}")
    if not sort:
        command.append("--no-sort")
    if repeat is not None:
        command.append(f"--repeat {repeat}")
    if quiet:
        command.append("-q")

    command.append(file)
    print(" ".join(command))
    # Execute command
    subprocess.run(" ".join(command), shell=True)


import re
import subprocess

def get_video_info(filepath):
    # Run ffmpeg command to get video information
    command = ['ffmpeg', '-i', filepath]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.communicate()[0].decode("utf-8")

    # Use regular expressions to extract the video information
    width_pattern = r"Stream .* Video: .* (\d+)x(\d+)"
    width_match = re.search(width_pattern, output)

    height_pattern = r"Stream .* Video: .* (\d+)x(\d+)"
    height_match = re.search(height_pattern, output)

    fps_pattern = r"Stream .* Video: .* (\d+\.?\d*) fps"
    fps_match = re.search(fps_pattern, output)

    duration_pattern = r"Duration: (\d+:\d+:\d+.\d+)"
    duration_match = re.search(duration_pattern, output)

    if width_match and height_match and fps_match and duration_match:
        width = int(width_match.group(1))
        height = int(height_match.group(2))
        fps = float(fps_match.group(1))
        duration = duration_match.group(1)
        return width, height, fps, duration
    else:
        return None
    


def begin(path):
    # if already exists
    dst_file = os.path.join(path+'.gif')
    if os.path.exists(dst_file): return

    try: shutil.rmtree(tmp_path)
    except: pass
    os.makedirs(tmp_path)
    subprocess.run(f"ffmpeg -i {path} -vf fps={image_fps} {tmp_path}/frame%04d.png", shell=True)
    width, height, video_fps, duration = get_video_info(path)

    fps_ = int( image_fps * speed_multiply )
    def evaluate(i):    # i = 0, 1, 2, ..., 100
        assert i != 0
        ratio = i / 100
        width_ = int((ratio*(max_width_limit-min_width_limit) + min_width_limit)*width) 
        dst_file = os.path.join(path+'.tmp.gif')
        dst_file_final = os.path.join(path+'.gif')
        create_gif(dst_file, file=f"{tmp_path}/frame*.png", fps=fps_, width=width_, quality=i)
        file_size_bytes = os.path.getsize(dst_file)
        file_size_mb = file_size_bytes / (1024 ** 2)
        print(f'level {i}, size {file_size_mb} MB')
        dst_file = os.path.join(f+'.tmp.gif')
        dst_file_final = os.path.join(f+'.gif')
        try: os.remove(dst_file_final)
        except: pass
        os.rename(dst_file, dst_file_final)
        return file_size_mb - target_size_mb

    res = bi_search(fn=evaluate, range=range(1,101))

for f in to_do_list:
    begin(f)



"""
https://gif.ski by Kornel Lesiński

Usage: gifski [OPTIONS] --output <a.gif> <FILES>...

Arguments:
  <FILES>...  PNG image files for the animation frames

Options:
  -o, --output <a.gif>          Destination file to write to; "-" means stdout
  -r, --fps <num>               Frame rate of animation. If using PNG files as input, this means the speed, as all frames are kept. 
      --fast                    50% faster encoding, but 10% worse quality and larger file size
      --extra                   50% slower encoding, but 1% better quality
  -Q, --quality <1-100>         Lower quality may give smaller file [default: 90]
      --motion-quality <1-100>  Lower values reduce motion
      --lossy-quality <1-100>   Lower values introduce noise and streaks
  -W, --width <px>              Maximum width.
                                By default anims are limited to about 800x600
  -H, --height <px>             Maximum height (stretches if the width is also set)
      --no-sort                 Use files exactly in the order given, rather than sorted
  -q, --quiet                   Do not display anything on standard output/console
      --repeat <num>            Number of times the animation is repeated (-1 none, 0 forever or <value> repetitions
  -h, --help                    Print help
  -V, --version                 Print version

"""
