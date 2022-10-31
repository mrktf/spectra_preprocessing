import time

begin_time = time.time()

from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

type_of_input = str(
    input(
        "Do you want to input parameters as a list, or separately? Select L/S:\n"
    ))
while (type_of_input != "L" and type_of_input != "l" and type_of_input != "S"
       and type_of_input != "s"):
    type_of_input = str(input("Input error - please select L/S:\n"))
if type_of_input == "L" or type_of_input == "l":

    user_input = [
        item for item in input(
            f"Select the directory and parameters for spectra preprocessing separated by spaces:\n(directory or file path, preprocess complete directory?, minimum of x axis, maximum of x axis, x data step, export decimal separator.\n\n INPUT EXAMPLE: 'C:/Users/Me/MySpectra/ Y 500 2000 1 , Y 30/11/2021'\n\ndirectory or file path\t-\tSelect a .asc file (i.e. C:/Users/Me/MySpectra/spectrum1.asc) or a directory (i.e. C:/Users/Me/MySpectra/) to preprocess for data analysis.\npreprocess complete directory?\t-\tDo you want to convert all files in the selected directory? Y/N\nminimum of x axis\t-\tSelect the parameters for spectra truncation and interpolation - minimum of x axis (i.e. 500).\nmaximum of x axis\t-\tSelect the parameters for spectra truncation and interpolation - maximum of x axis (i.e. 2000).\nx data step\t-\tSelect the parameters for spectra truncation and interpolation - data step of x axis (i.e. 0.2 or 1).\nexport decimal separator\t-\tSelect the final decimal separator (, or .) for exported data (for Unscrambler comma is recommended).\n"
        ).split()
    ]

    input_path = str(user_input[0])
    iterate = str(user_input[1])
    minimum = int(user_input[2])
    maximum = int(user_input[3])
    step = float(user_input[4])
    final_dec_separator = str(user_input[5])

    while iterate != "Y" and iterate != "N" and iterate != "y" and iterate != "n":
        print("Please select Y or N!\n")
        iterate = str(
            input(
                "Do you want to convert all files in the selected directory? Y/N\n"
            ))
    while minimum <= 200:
        minimum = int(input("Select valid minimum of x axis (i.e. 500):\n"))
    while maximum <= 600:
        maximum = int(input("Select valid maximum of x axis (i.e. 2000):\n"))
    while step not in [0.5, 1, 2, 4]:
        step = float(
            input(
                "Select valid data step of x axis (i.e. 0.1, 0.2, 0.25, 0.5, 1, 2, 4 or 5):\n"
            ))
    no_x_points = int((maximum - minimum) / step + 1)
    print(f"Number of datapoints will be {no_x_points}.\n")

else:
    # DIRECTORY
    input_path = str(
        input(
            "Select a .asc file (i.e. C:/Users/Me/MySpectra/spectrum1.asc) or a directory (i.e. C:/Users/Me/MySpectra/) to preprocess for data analysis:\n"
        ))

    iterate = str(
        input(
            "Do you want to convert all files in the selected directory? Y/N\n"
        ))
    while iterate != "Y" and iterate != "N" and iterate != "y" and iterate != "n":
        print("Please select Y or N!\n")
        iterate = str(
            input(
                "Do you want to convert all files in the selected directory? Y/N\n"
            ))

    # MIN/MAX VALUES OF X AXIS
    minimum = int(
        input(
            "Select the parameters for spectra truncation and interpolation - minimum of x axis (i.e. 500):\n"
        ))
    while minimum <= 200:
        minimum = int(input("Select valid minimum of x axis (i.e. 500):\n"))

    maximum = int(
        input(
            "Select the parameters for spectra truncation and interpolation - maximum of x axis (i.e. 2000):\n"
        ))
    while maximum <= 600:
        maximum = int(input("Select valid maximum of x axis (i.e. 2000):\n"))

    # DESIRED DATASTEP OF X AXIS
    step = float(
        input(
            "Select the parameters for spectra truncation and interpolation - data step of x axis (i.e. 0.5 or 1):\n"
        ))
    while step not in [0.5, 1, 2, 4]:
        step = float(
            input(
                "Select suitable data step of x axis (i.e. 0.5, 1, 2 or 4):\n")
        )
    no_x_points = int((maximum - minimum) / step + 1)
    print(f"Number of datapoints will be {no_x_points}.\n")

    # SELECTION OF DECIMAL SEPARATOR OF EXPORTED FILES
    final_dec_separator = str(
        input(
            "Select the final decimal separator (, or .) for exported data (for Unscrambler comma is recommended):\n"
        ))
    while final_dec_separator != "," and final_dec_separator != ".":
        final_dec_separator = str(
            input("Select valid decimal separator (, or .):\n"))

if iterate == "Y" or iterate == "y":
    # creation of a list of files to preprocess
    filelist = []
    for file in glob.glob(f"{input_path}*.txt"):
        # creation of list of filenames in the directory
        filename = os.path.basename(file)
        filelist.append(filename)
    print(filelist)
    # loop for all files in the directory
    for filename in filelist:
        # replacement of decimal separator in original file
        iterated_path = f"{input_path}{filename}"
        search_text = ","
        replace_text = "."
        with open(iterated_path, "r") as file:
            data = file.read()
            data = data.replace(search_text, replace_text)
        with open(iterated_path, "w+", encoding="ANSI") as file:
            file.write(data)
            file.close()

        # # # # # # # # # # # # # # # # # # # # # #
        # # SPECTRUM IMPORT AND DEFINITION OF X,Y #
        # # # # # # # # # # # # # # # # # # # # # #

        spectrum_array = np.loadtxt(iterated_path, skiprows=15, delimiter="\t")
        spectrum_list = np.ndarray.tolist(spectrum_array)
        len_sp_list = len(spectrum_list)

        x = []
        for i in range(0, len_sp_list):
            array_row = spectrum_list[i]

            x.append(float(array_row[0]))

        y = []
        for i in range(0, len_sp_list):
            array_row = spectrum_list[i]
            y.append(int(array_row[1]))

        # # # # # # # # # # # # # # # # # #
        # #  INTERPOLATION,TRUNCATION # # #
        # # # # # # # # # # # # # # # # # #

        f = CubicSpline(x, y, bc_type="natural")
        x_new = np.linspace(minimum, maximum, no_x_points)
        y_new = f(x_new)

        # FFT the signal
        sig_fft = np.fft.fft(y_new)
        # copy the FFT results
        sig_fft_filtered = sig_fft.copy()
        # obtain the frequencies using scipy function
        freq = np.fft.fftfreq(len(y_new), d=1. / 6555)
        # define the cut-off frequency
        cut_off = 19

        # low-pass filter by assign zeros to the FFT amplitudes where the absolute frequencies higher than the cut-off
        sig_fft_filtered[np.abs(freq) > cut_off] = 0

        # get the filtered signal in orig domain
        filter = np.fft.ifft(sig_fft_filtered)
        filtered = np.real(filter)

        filename_final = iterated_path[:-4] + "_bl.txt"
        final_txt_file = open(filename_final, "w+")
        for i in range(0, no_x_points):
            final_txt_file.write(f"{x_new[i]};{filtered[i]}\n")
        final_txt_file.close()
        # export of file with commas as a decimal separator
        if final_dec_separator == ",":
            with open(filename_final, "r") as file:
                data = file.read()
                data = data.replace(replace_text, search_text)
            with open(filename_final, "w+", encoding="ANSI") as file:
                file.write(data)
            file.close()

    print(
        f"{len(filelist)} spectra were successfully preprocessed and exported as semicolon separated ASCII txt files."
    )
elif iterate == "N" or iterate == "n":
    # SINGLE FILE PREPROCESSING
    # replacement of decimal separator in original file
    search_text = ","
    replace_text = "."
    with open(input_path, "r") as file:
        data = file.read()
        data = data.replace(search_text, replace_text)
    with open(input_path, "w+", encoding="ANSI") as file:
        file.write(data)
        file.close()
    ascii_grid = np.loadtxt(input_path, skiprows=15, delimiter="\t")
    ascii_grid_data = np.ndarray.tolist(ascii_grid)

    # # # # # # # # # # # # # # # # # # # # # #
    # SPECTRUM IMPORT AND DEFINITION OF X,Y # #
    # # # # # # # # # # # # # # # # # # # # # #

    spectrum_array = np.loadtxt(input_path, skiprows=15, delimiter="\t")

    spectrum_list = np.ndarray.tolist(spectrum_array)
    len_sp_list = len(spectrum_list)
    x = []
    for i in range(0, len_sp_list):
        array_row = spectrum_list[i]

        x.append(float(array_row[0]))

    y = []
    for i in range(0, len_sp_list):
        array_row = spectrum_list[i]
        y.append(int(array_row[1]))

    plt.title(f"Raw as collected ROA Spectrum")
    plt.xlabel(f"Raman shift (cm\u207b\u00b9)")
    plt.ylabel("Counts")
    plt.plot(x, y, "blue")
    plt.show()

    # # # # # # # # # # # # # # # # # #
    # #  INTERPOLATION,TRUNCATION   # #
    # # # # # # # # # # # # # # # # # #

    # # use bc_type = 'natural' adds the constraints as we described above
    f = CubicSpline(x, y, bc_type="natural")
    x_new = np.linspace(minimum, maximum, no_x_points)
    y_new = f(x_new)

    plt.title(
        f"Interpolated ROA Spectrum {minimum}\u2014{maximum} cm\u207b\u00b9")
    plt.xlabel(f"Raman shift (cm\u207b\u00b9)")
    plt.ylabel("Counts")
    plt.plot(x_new, y_new, "orange")
    plt.show()

    # FFT the signal
    sig_fft = np.fft.fft(y_new)
    # copy the FFT results
    sig_fft_filtered = sig_fft.copy()
    # obtain the frequencies using scipy function
    freq = np.fft.fftfreq(len(y_new), d=1. / 6555)
    # define the cut-off frequency
    cut_off = 19

    # low-pass filter by assign zeros to the FFT amplitudes where the absolute frequencies higher than the cut-off
    sig_fft_filtered[np.abs(freq) > cut_off] = 0

    # get the filtered signal in orig domain
    filter = np.fft.ifft(sig_fft_filtered)
    filtered = np.real(filter)

    plt.figure()
    plt.title("FFT of the ROA Spectrum")
    plt.xlabel("Raman shift (cm\u207b\u00b9)")
    plt.ylabel("Counts")
    plt.plot(x_new, y_new, "grey", label="original signal")
    plt.plot(x_new, filtered, "yellow", label="FFT filtered signal")
    plt.legend()
    plt.show()

    filename_final = input_path[:-4] + "_bl.txt"
    final_txt_file = open(filename_final, "w+")
    for i in range(0, no_x_points):
        final_txt_file.write(f"{x_new[i]};{filtered[i]}\n")
    final_txt_file.close()
    # export of file with commas as a decimal separator
    if final_dec_separator == ",":
        with open(filename_final, "r") as file:
            data = file.read()
            data = data.replace(replace_text, search_text)
        with open(filename_final, "w+", encoding="ANSI") as file:
            file.write(data)
        file.close()

    print(
        f"Spectrum was successfully preprocessed and exported as:\n{filename_final}\n\t- semicolon separated ASCII txt files.\n"
    )
else:
    print(f"Input error, try again.\n")
time.sleep(1)
end_time = time.time()
print(f"Finished in {end_time - begin_time} seconds")