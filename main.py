import os
import dearpygui.dearpygui as dpg
import tkinter.filedialog

import traceback
import converter

def open_dir(sender, app_data, user_data):
    if user_data == "asbtojson_output":
        dpg.set_value("asbtojson_output", tkinter.filedialog.askdirectory())
    if user_data == "jsontoasb_output":
        dpg.set_value("jsontoasb_output", tkinter.filedialog.askdirectory())

    if user_data == "romfs":
        path = tkinter.filedialog.askdirectory()
        with open("romfs.txt", "w", encoding="utf-8") as f:
            f.write(path)
            f.close()
        dpg.set_value("romfs", "RomFS path: " + path)
        

def open_file(sender, app_data, user_data):
    if user_data == "asbtojson_input":
        dpg.set_value("asbtojson_input", tkinter.filedialog.askopenfilename(
            title = "ASB to JSON input asb file",
            filetypes = (("idk what asb stands for","*.asb"),("all files","*.*")))
        )

    if user_data == "jsontoasb_input":
        dpg.set_value("jsontoasb_input", tkinter.filedialog.askopenfilename(
            title = "JSON to ASB input file",
            filetypes = (("JSON stands for JavaScript Object Notation","*.json"),("all files","*.*")))
        )

    if user_data == "baevtojson_input":
        dpg.set_value("baevtojson_input", tkinter.filedialog.askopenfilename(
            title = "BAEV to JSON input file",
            filetypes = (("idk what baev stands for","*.baev"),("all files","*.*")))
        )


    if user_data == "jsontobaev_input":
        dpg.set_value("jsontobaev_input", tkinter.filedialog.askopenfilename(
            title = "JSON to BAEV input file",
            filetypes = (("JSON stands for JavaScript Object Notation","*.json"),("all files","*.*")))
        )

def conversion_stuff(sender, app_data, user_data):
    try:
        if user_data == "asbtojson":
            converter.asb_to_json(dpg.get_value("asbtojson_input"), dpg.get_value("asbtojson_output"))
        if user_data == "jsontoasb":
            converter.json_to_baev(dpg.get_value("jsontoasb_input"), dpg.get_value("jsontoasb_output"))
        if user_data == "baevtojson":
            converter.baev_to_json(dpg.get_value("baevtojson_input"))
        if user_data == "jsontobaev":
            converter.json_to_baev(dpg.get_value("jsontobaev_input"))
        
    except Exception as e:
        dpg.set_value("error_output", traceback.format_exc())

def init_dpg():
    dpg.create_context()

    with dpg.window(tag="MainWindow") as window:
        # messy error handler
        errorhandlertheme = dpg.add_theme()
        with dpg.theme_component(dpg.mvText,parent=errorhandlertheme):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 120, 120), category=dpg.mvThemeCat_Core)

        with dpg.collapsing_header(tag="romfsheader", label="RomFS"):
            romFSPath = ""
            if os.path.exists("romfs.txt"):
                with open("romfs.txt", "r", encoding="utf-8") as f:
                    romFSPath = f.read()
                    f.close()
            
            dpg.add_text("RomFS path: " + romFSPath, tag="romfs")
            dpg.add_button(label="Browse for RomFS folder", callback=open_dir, user_data="romfs")

        with dpg.collapsing_header(tag="asbtojson", label="ASB to JSON"):
            dpg.add_button(label="Browse for input ASB file", callback=open_file, user_data="asbtojson_input")
            dpg.add_text(tag="asbtojson_input", default_value="Input file placeholder")
            dpg.add_button(label="Browse for output folder (optional)", callback=open_dir, user_data="asbtojson_output")

            dpg.add_text(tag="asbtojson_output", default_value="Output folder placeholder")
            dpg.add_button(label="Convert", callback=conversion_stuff, user_data="asbtojson")

        with dpg.collapsing_header(tag="jsontoasb", label="JSON to ASB"):
            dpg.add_button(label="Browse for input JSON file", callback=open_file, user_data="jsontoasb_input")
            dpg.add_text(tag="jsontoasb_input", default_value="Input file placeholder")
            dpg.add_button(label="Browse for output folder (optional)", callback=open_dir, user_data="jsontoasb_output")

            dpg.add_text(tag="jsontoasb_output", default_value="Output folder placeholder")
            dpg.add_button(label="Convert", callback=conversion_stuff, user_data="jsontoasb")

        with dpg.collapsing_header(tag="baevtojson", label="BAEV to JSON"):
            dpg.add_button(label="Browse for input baev file", callback=open_file, user_data="baevtojson_input")
            dpg.add_text(tag="baevtojson_input", default_value="Input file placeholder")

            dpg.add_button(label="Convert", callback=conversion_stuff, user_data="baevtojson")

        with dpg.collapsing_header(tag="jsontobaev", label="JSON to BAEV"):
            dpg.add_button(label="Browse for input JSON file", callback=open_file, user_data="jsontobaev_input")
            dpg.add_text(tag="jsontobaev_input", default_value="Input file placeholder")

            dpg.add_button(label="Convert", callback=conversion_stuff, user_data="jsontobaev")
    
    
        error_output = dpg.add_text(tag="error_output", default_value="errors display here")
        dpg.bind_item_theme(error_output, errorhandlertheme)
    dpg.create_viewport(title="ASB worker GUI", width=300, height=400)
    dpg.setup_dearpygui()
    dpg.set_primary_window(window, True)

if __name__ == "__main__":
    init_dpg()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()