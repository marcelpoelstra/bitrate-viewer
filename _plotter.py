import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

from _utils import get_mbit_str, get_pretty_codec_name


def plot_results(results, graph_title, graph_filename):
    seconds, bitrates, keyframes, encoder, gop_sizes = results

    number_of_keyframes = len(keyframes)
    if number_of_keyframes > 75:
        print(f'Warning:\n{str(number_of_keyframes)} I-Frames detected.\n'
              'I-Frames are not shown on the graph for a video with more '
              'than 75 I-Frames as this results in a cluttered graph.\n'
              'Plotting the bitrate graph without I-frame markings...')
        # drop keyframes
        keyframes = []

    avg_bitrate = get_mbit_str(round(np.mean(bitrates), 2))
    min_bitrate = get_mbit_str(round(min(bitrates), 2))
    max_bitrate = get_mbit_str(round(max(bitrates), 2))
    std_bitrate = get_mbit_str(round(np.std(bitrates), 2))
    encoder = get_pretty_codec_name(encoder)

    # calculate the GoP sizes in kBytes
    gop_sizes = [int(size / 1024) for size in gop_sizes]

    # init the plot
    plt.figure(figsize=(19.20, 10.80))
    plt.suptitle(f'{graph_title} | Codec: {encoder}\n\
                Min: {min_bitrate} | Max: {max_bitrate} | Standard Deviation: '
                 f'{std_bitrate}')
    plt.xlabel('Seconds')
    plt.ylabel('Video Bitrate (Mbps)')
    plt.grid(True)

    # actually plot the data
    bitrate_line, = plt.plot(seconds, bitrates,
                             label=f'Bitrate (Average: {avg_bitrate})')
    # plot vertical lines for keyframes
    for i, frame in enumerate(keyframes):
        plt.axvline(frame, color='r', linestyle='--', linewidth=1)
        # add GoP size text
        if i < len(gop_sizes):
            plt.text(frame, max(bitrates) * 0.95,
                     f' Size I-I {gop_sizes[i]} kBytes', ha='left', va='top')

    # create legend for I-frame-lines
    label_text = 'I-Frames' if number_of_keyframes <= 75 else \
                 'Too many I-Frames'
    i_frame_legend = mlines.Line2D([], [], color='red', linestyle='--',
                                   markersize=10, label=label_text)
    # setup plot legend
    plt.legend(handles=[bitrate_line, i_frame_legend],
               labels=[bitrate_line.get_label(),
                       i_frame_legend.get_label()],
               loc='lower right')

    # save the plot
    plt.savefig(f'{graph_filename}_bitrate.png')
