from GutGuiModules import *
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    (window, input_output, image_diagram) = init()

    listener = ModuleListener()

    # source and output
    source_and_output_frame = frame(input_output, PASTEL_BLUE_RGB, 0, 0, 1, 2)
    source_and_output_module = SourceAndOutput(source_and_output_frame, listener)
    listener.attach_module(SOURCE_AND_OUTPUT, source_and_output_module)

    # analysis and form
    analysis_and_form_frame = frame(input_output, PASTEL_ORANGE_RGB, 1, 0, 1, 2)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame, listener)
    listener.attach_module(ANALYSIS_AND_FORM, analysis_and_form_module)

    # save
    save_frame = frame(input_output, PASTEL_PINK_RGB, 2, 0, 1, 1)
    save_module = Save(save_frame, listener)
    listener.attach_module(SAVE, save_module)

    # info
    info_frame = frame(input_output, PASTEL_PINK_RGB, 2, 1, 1, 1)
    info_module = Info(info_frame, listener)
    listener.attach_module(INFO, info_module)

    # save csvs
    csv_frame = frame(input_output, PASTEL_PINK_RGB, 0, 2, 3, 1)
    csv_module = CSVSaver(csv_frame, listener)
    listener.attach_module(CSV, csv_module)

    # original colour
    og_color_frame = frame(image_diagram, PASTEL_PINK_RGB, 0, 0, 7, 6)
    og_color_module = OGColour(og_color_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR, og_color_module)

    # original colour data
    og_color_data_frame = frame(image_diagram, PASTEL_PINK_RGB, 2, 12, 3, 2)
    og_color_data_module = OGColourData(og_color_data_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR_DATA, og_color_data_module)

    # recreated colour
    recreated_color_frame = frame(image_diagram, PASTEL_BLUE_RGB, 7, 0, 7, 3)
    recreated_color_module = RecColour(recreated_color_frame, listener)
    listener.attach_module(RECREATED_COLOUR, recreated_color_module)

    # recreated colour data
    rec_color_data_frame = frame(image_diagram, PASTEL_ORANGE_RGB, 5, 12, 4, 2)
    rec_color_data_module = RecreatedColourData(rec_color_data_frame, listener)
    listener.attach_module(RECREATED_COLOUR_DATA, rec_color_data_module)

    # new colour
    new_color_frame = frame(image_diagram, PASTEL_ORANGE_RGB, 7, 3, 7, 3)
    new_color_module = NewColour(new_color_frame, listener)
    listener.attach_module(NEW_COLOUR, new_color_module)

    # new colour data
    new_color_data_frame = frame(image_diagram, PASTEL_BLUE_RGB, 9, 12, 3, 2)
    new_color_data_module = NewColourData(new_color_data_frame, listener)
    listener.attach_module(NEW_COLOUR_DATA, new_color_data_module)

    # diagram
    diagram_frame = frame(image_diagram, PASTEL_ORANGE_RGB, 0, 12, 2, 2)
    diagram_module = Diagram(diagram_frame, listener)
    listener.attach_module(DIAGRAM, diagram_module)

    # histogram
    histogram_frame = frame(image_diagram, PASTEL_BLUE_RGB, 0, 6, 8, 6)
    histogram_module = Histogram(histogram_frame, listener)
    listener.attach_module(HISTOGRAM, histogram_module)

    # absorption
    absorption_spec_frame = frame(image_diagram, PASTEL_PINK_RGB, 8, 6, 6, 6)
    absorption_module = AbsorptionSpec(absorption_spec_frame, listener)
    listener.attach_module(ABSORPTION_SPEC, absorption_module)

    # colourbar
    colour_frame = frame(image_diagram, PASTEL_PINK_RGB, 12, 12, 2, 2)
    colour_module = Colour(colour_frame, listener)

    window.mainloop()

if __name__ == '__main__':
    main()
