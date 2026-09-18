import os
import subprocess
import imageio_ffmpeg

ff = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs('output/test_act1', exist_ok=True)

shots = [
    ('assets/scenes/shot_01_ground_feet.jpg', 'output/test_act1/shot_01.mp4', 7.5,
     "zoompan=z='min(zoom+0.0008,1.15)':x='(iw/2-(iw/zoom/2))+sin(on*0.25)*8':y='(ih/2-(ih/zoom/2))+abs(sin(on*0.35))*6':d=225:s=1920x1080:fps=30,eq=contrast=1.05:saturation=1.05,format=yuv420p"),
    ('assets/scenes/shot_02_volcanic_gas.jpg', 'output/test_act1/shot_02.mp4', 9.0,
     "zoompan=z='min(zoom+0.0006,1.18)':x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom, on*0.5)':d=270:s=1920x1080:fps=30,eq=contrast='1.08+sin(n*0.1)*0.04':saturation=1.15:brightness='if(between(mod(n,85),0,2),0.35,0)',format=yuv420p"),
    ('assets/scenes/shot_03_theia_approach.jpg', 'output/test_act1/shot_03.mp4', 10.0,
     "zoompan=z='min(zoom+0.0016,1.30)':x='iw*0.58-(iw/zoom/2)':y='ih*0.55-(ih/zoom/2)':d=300:s=1920x1080:fps=30,eq=contrast=1.08:saturation=1.10,format=yuv420p"),
    ('assets/scenes/theia_impact.jpg', 'output/test_act1/shot_04.mp4', 7.0,
     "zoompan=z='min(zoom+0.0025,1.35)':x='iw*0.50-(iw/zoom/2)':y='ih*0.48-(ih/zoom/2)':d=210:s=1920x1080:fps=30,eq=contrast=1.10:saturation=1.15,format=yuv420p"),
    ('assets/scenes/shot_04_theia_impact.jpg', 'output/test_act1/shot_05.mp4', 11.2,
     "zoompan=z='min(zoom+0.0012,1.25)':x='(iw/2-(iw/zoom/2))+sin(on*2.0)*max(0, 10 - on*0.06)':y='ih/2-(ih/zoom/2)':d=336:s=1920x1080:fps=30,eq=brightness='if(lt(n,12),0.85*(1-n/12),0)':contrast=1.12:saturation=1.18,format=yuv420p")
]

for idx, (img, out_path, dur, flt) in enumerate(shots, 1):
    cmd = [ff, '-y', '-loop', '1', '-i', img, '-vf', flt, '-c:v', 'libx264', '-preset', 'faster', '-crf', '19', '-t', str(dur), out_path]
    subprocess.run(cmd, check=True)
    print(f'Shot {idx} rendered: {round(os.path.getsize(out_path)/1024, 1)} KB')

# Concat shots
concat_file = 'output/test_act1/concat.txt'
with open(concat_file, 'w', encoding='utf-8') as f:
    for _, out_path, _, _ in shots:
        clean_p = os.path.abspath(out_path).replace('\\', '/')
        f.write(f"file '{clean_p}'\n")

merged = 'output/test_act1/act_01_multishot.mp4'
c_cmd = [ff, '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', merged]
subprocess.run(c_cmd, check=True)
print(f'Merged Act 1 Multi-shot: {round(os.path.getsize(merged)/1024/1024, 2)} MB')
