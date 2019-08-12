from GutGuiModules.utility import *
import numpy as np
from matplotlib.offsetbox import AnchoredText
from decimal import Decimal
import logging

class Histogram:
    def __init__(self, histogram_frame, listener):
        self.root = histogram_frame
        self.listener = listener

        self.flattened_data = None

        self.specs = (False, True, False)
        self.spec_number = 1

        self.parametric = False
        self.non_parametric = False

        self.parametric_button = None
        self.mean_text = None
        self.mean_value = None
        self.sd_text = None
        self.sd_value = None
        self.non_parametric_button = None
        self.median_text = None
        self.median_value = None
        self.iqr_text = None
        self.iqr_value = None

        self.first_line = None
        self.min_x = None
        self.min_x_val = None
        self.min_y = None
        self.min_y_val = None
        self.second_line = None
        self.max_x = None
        self.max_x_val = None
        self.max_y = None
        self.max_y_val = None

        self.none_button = None
        self.percent_negative_text = None
        self.percent_negative_value = None

        self.drop_down_var = StringVar()
        self.choices = ['1. Reflectance - Original', 
        '2. Reflectance - Original without Negative Values', 
        '3. Reflectance - Normalised',
        '4. Reflectance - Normalised without Negative Values', 
        '5. Absorbance - Original', 
        '6. Absorbance - Original without Negative Values', 
        '7. Absorbance - Normalised',
        '8. Absorbance - Normalised without Negative Values', 
        '9. Recreated Image', 
        '10. Recreated Image - Normalised',
        '11. New Image',
        '12. New Image - Normalised']

        self.x_upper_scale_text = None
        self.y_upper_scale_text = None
        self.x_lower_scale_text = None
        self.y_lower_scale_text = None
        self.x_upper_scale_input = None
        self.y_upper_scale_input = None
        self.x_lower_scale_input = None
        self.y_lower_scale_input = None
        self.x_upper_scale_value = None
        self.y_upper_scale_value = None
        self.x_lower_scale_value = None
        self.y_lower_scale_value = None

        self.step_size_text = None
        self.step_size_input = None
        self.step_size_value = 0.01 

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()
        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = IntVar()
        self.save_as_excel_label = None
        self.save_as_excel_checkbox = None
        self.save_as_excel_checkbox_value = IntVar()

        self.interactive_histogram_graph = None
        self.axes = None
        self.axes2 = None
        self.interactive_histogram = None

        self.upper_text = None
        self.upper_input = None
        self.upper_value = None
        self.lower_text = None
        self.lower_input = None
        self.lower_value = None

        self.info_label = None

        self._init_widgets()

    def get_specs(self):
        return self.specs

    def get_spec_number(self):
        return self.spec_number

    def get_step_size(self):
        return self.step_size_value

    def get_save_checkbox_value(self):
        return not bool(self.save_checkbox_value.get())

    def get_save_wo_scale_checkbox_value(self):
        return not bool(self.save_wo_scale_checkbox_value.get())

    def get_save_as_excel_checkbox_value(self):
        return not bool(self.save_as_excel_checkbox_value.get())

    def update_histogram(self, data):
        logging.debug("BUILDING HISTOGRAM...")
        self.flattened_data = data.flatten()
        self.flattened_data = self.flattened_data[self.flattened_data != np.array(None)]
        self.upper_value = np.ma.max(self.flattened_data)
        self.lower_value = np.ma.min(self.flattened_data)
        self._calc_stats()
        self._build_scale()
        self._build_interactive_histogram()

    # Helper

    def _init_widgets(self):
        self._build_scale()
        self._build_step_size()
        self._build_save()
        self._build_save_wo_scale()
        self._build_save_as_excel()
        self._build_info_label()
        self._build_reset_button()
        self._build_drop_down()
        self._build_interactive_histogram()
        self._build_stats()

    def _build_stats(self):
        # parametric
        self.parametric_button = make_button(self.root, text='P:', width=4, command=self.__parametric, column=0, row=2, columnspan=1, outer_padx=(15, 0), highlightthickness=0, inner_padx=3, inner_pady=0, outer_pady=(0, 3))
        # mean
        self.mean_text = make_text(self.root, content="Mean = " + str(self.mean_value), bg=tkcolour_from_rgb(BACKGROUND), column=1, row=2, width=12, columnspan=1, padx=0, state=NORMAL)
        # standard deviation
        self.sd_text = make_text(self.root, content="SD = " + str(self.sd_value), bg=tkcolour_from_rgb(BACKGROUND), column=2, row=2, width=10, columnspan=1, padx=0, state=NORMAL)
        # non parametric
        self.non_parametric_button = make_button(self.root, text='NP:', width=4, command=self.__non_parametric, column=0, row=3, columnspan=1, outer_padx=(15, 0), highlightthickness=0, inner_padx=3, inner_pady=0)
        # median
        self.median_text = make_text(self.root, content="Median = " + str(self.median_value), bg=tkcolour_from_rgb(BACKGROUND), column=1, row=3, width=14, columnspan=1, padx=0, state=NORMAL)
        # IQR
        self.iqr_text = make_text(self.root, content="IQR = " + str(self.iqr_value), bg=tkcolour_from_rgb(BACKGROUND), column=2, row=3, width=22, columnspan=1, padx=(0, 10), state=NORMAL)
        # min and max
        first_line_text = "x min = " + str(self.min_x) + ', y val = ' + str(self.min_x_val) + '      y min = ' + str(self.min_y) + ', x val = ' + str(self.min_y_val)
        self.first_line = make_text(self.root, content=first_line_text, bg=tkcolour_from_rgb(BACKGROUND), column=1, row=4, width=60, columnspan=4, state=NORMAL, pady=(10, 0))
        second_line_text = "x max = " + str(self.max_x) + ', y val = ' + str(self.max_x_val) + '      y max = ' + str(self.max_y) + ', x val = ' + str(self.max_y_val)
        self.second_line = make_text(self.root, content=second_line_text, bg=tkcolour_from_rgb(BACKGROUND), column=1, row=5, width=60, columnspan=4, state=NORMAL, pady=(0, 20))
        # none
        self.none_button = make_button(self.root, text='None', width=4, command=self.__none, column=0, row=1, columnspan=1, outer_padx=(15, 0), outer_pady=(0,3), highlightthickness=0, inner_padx=3, inner_pady=0)
        # percent negative
        self.percent_negative_text = make_text(self.root, content="% Negative = " + str(self.percent_negative_value) + '%', bg=tkcolour_from_rgb(BACKGROUND), column=3, row=2, width=25, columnspan=2, rowspan=2, padx=(10, 0), state=NORMAL, pady=0)

    def _build_drop_down(self):
        self.drop_down_var.set(self.choices[0])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__update_data)
        self.drop_down_menu.configure(highlightthickness=0, width=6, 
            anchor='w', padx=15)
        self.drop_down_menu.grid(column=1, row=0, columnspan=1, padx=(0, 15))

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=13, column=0,inner_padx=10, inner_pady=5, outer_padx=(15, 10), outer_pady=(0, 15))
        self.save_checkbox = make_checkbox(self.root, "", row=13, column=0, var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=13, column=1, inner_padx=10, inner_pady=5, outer_padx=(10, 16), outer_pady=(0, 15))
        self.save_wo_scale_checkbox = make_checkbox(self.root, "", row=13, column=1, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0,12))
        self.save_wo_scale_checkbox.deselect()
        self.save_wo_scale_checkbox.bind('<Button-1>', self.__update_save_wo_scale_check_status)

    def _build_save_as_excel(self):
        self.save_as_excel_label = make_label(self.root, "Save as CSV", row=13, column=2, inner_padx=10, inner_pady=5, outer_padx=(5, 15), outer_pady=(0, 15))
        self.save_as_excel_checkbox = make_checkbox(self.root, "", row=13, column=2,var=self.save_as_excel_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 9))
        self.save_as_excel_checkbox.deselect()
        self.save_as_excel_checkbox.bind('<Button-1>', self.__update_save_as_excel_check_status)

    def _build_reset_button(self):
        self.reset_button = make_button(self.root, "Reset", row=13, column=3, command=self.__reset, inner_padx=10, inner_pady=5, outer_padx=15, outer_pady=(0, 10), columnspan=2)

    def _build_scale(self):
        # lower
        self.lower_text = make_text(self.root, content="Lower: ", 
            bg=tkcolour_from_rgb(BACKGROUND), column=3, row=7, width=7, columnspan=1, pady=(0, 10))
        self.lower_input = make_entry(self.root, row=7, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.lower_input.bind('<Return>', self.__update_upper_lower)
        self.lower_input.insert(END, str(self.min_x))

        # upper
        self.upper_text = make_text(self.root, content="Upper: ", 
            bg=tkcolour_from_rgb(BACKGROUND), column=3, row=8, width=7, columnspan=1, pady=(0, 10))
        self.upper_input = make_entry(self.root, row=8, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.upper_input.bind('<Return>', self.__update_upper_lower)
        self.upper_input.insert(END, str(self.max_x))

        # x lower
        self.x_lower_scale_text = make_text(self.root, content="Min x: ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=9, width=7, columnspan=1, pady=(0, 10))
        self.x_lower_scale_input = make_entry(self.root, row=9, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_lower_scale_input.bind('<Return>', self.__update_scales)
        self.x_lower_scale_input.insert(END, str(self.min_x))

         # x upper
        self.x_upper_scale_text = make_text(self.root, content="Max x: ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=10, width=7, columnspan=1, pady=(0, 10))
        self.x_upper_scale_input = make_entry(self.root, row=10, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.x_upper_scale_input.bind('<Return>', self.__update_scales)
        self.x_upper_scale_input.insert(END, str(self.max_x))

        # y lower
        self.y_lower_scale_text = make_text(self.root, content="Min y: ", bg=tkcolour_from_rgb(BACKGROUND),column=3, row=11, width=7, columnspan=1, pady=(0, 10))
        self.y_lower_scale_input = make_entry(self.root, row=11, column=4, width=7, pady=(0, 10), padx=(0, 15),columnspan=1)
        self.y_lower_scale_input.bind('<Return>', self.__update_scales)
        self.y_lower_scale_input.insert(END, str(self.min_y))

        # y upper
        self.y_upper_scale_text = make_text(self.root, content="Max y: ", bg=tkcolour_from_rgb(BACKGROUND), column=3, row=12, width=7, columnspan=1, pady=(0, 10))
        self.y_upper_scale_input = make_entry(self.root, row=12, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.y_upper_scale_input.bind('<Return>', self.__update_scales)
        self.y_upper_scale_input.insert(END, str(self.max_y))

    def _build_step_size(self):
        self.step_size_text = make_text(self.root, content="Step: ", 
            bg=tkcolour_from_rgb(BACKGROUND), column=3, row=6, width=6, columnspan=1, pady=(0, 10))
        self.step_size_input = make_entry(self.root, row=6, column=4, width=7, pady=(0, 10), padx=(0, 15), columnspan=1)
        self.step_size_input.bind('<Return>', self.__update_scales)
        self.step_size_input.insert(END, str(self.step_size_value))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Histogram', command=self.__info, width=8)

    def _build_interactive_histogram(self):
        # create canvas
        self.interactive_histogram_graph = Figure(figsize=(3.5, 2))
        self.axes = self.interactive_histogram_graph.add_subplot(111)
        self.interactive_histogram_graph.patch.set_facecolor(rgb_to_rgba(BACKGROUND))
        if self.flattened_data is not None:
            # calc bins
            bins = np.arange(start = np.ma.min(self.flattened_data), stop = np.ma.max(self.flattened_data) + self.step_size_value, step = self.step_size_value)
            # plot histogram
            self.axes.hist(self.flattened_data, bins=bins)
            if self.parametric == True:
                # plot error bar
                self.axes2 = self.axes.twinx()
                self.axes2.plot([self.mean_value-self.sd_value, self.mean_value+self.sd_value], [1, 1], 'k-', lw=1)
                self.axes2.plot([self.mean_value-self.sd_value, self.mean_value-self.sd_value], [0.9, 1.1], 'k-', lw=1)
                self.axes2.plot([self.mean_value+self.sd_value, self.mean_value+self.sd_value], [0.9, 1.1], 'k-', lw=1)
                self.axes2.plot([self.mean_value, self.mean_value], [0.9, 1.1], '#F17E3A', lw=1)
                self.axes2.set_ylim(bottom=0, top=2)
                self.axes2.get_yaxis().set_visible(False)
            elif self.non_parametric == True:
                # plot boxplot
                self.axes2 = self.axes.twinx()
                self.axes2.boxplot(self.flattened_data, vert=False, sym='')
                self.axes2.get_yaxis().set_visible(False)
            # set axes
            self.interactive_histogram_graph.set_tight_layout(True)
            self.axes.set_xlim(left=self.x_lower_scale_value, right=self.x_upper_scale_value)
            self.axes.set_ylim(bottom=self.y_lower_scale_value, top=self.y_upper_scale_value)
            # commas and non-scientific notation
            self.axes.ticklabel_format(style='plain')
            self.axes.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',') if x%1==0 else format(float(x))))
            self.axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',') if x%1==0 else format(float(x))))

        # draw figure
        self.interactive_histogram = FigureCanvasTkAgg(self.interactive_histogram_graph, master=self.root)
        self.interactive_histogram.draw()
        self.interactive_histogram.get_tk_widget().grid(column=0, row=6, columnspan=3, rowspan=7, ipady=5, ipadx=0, pady=0)
        self.interactive_histogram.get_tk_widget().bind('<Button-2>', self.__pop_up_image)

    def _calc_stats(self):
        # construct data list in proper range
        logging.debug("CONSTRUCTING RANGED DATA...")
        data = self.flattened_data[self.lower_value <= self.flattened_data]
        data = data[data <= self.upper_value]
        # mean, sd, median, iqr
        logging.debug("CALCULATING STATS...")
        self.mean_value = np.round(np.ma.mean(data), 3)
        progress(0, 11)
        self.sd_value = np.round(np.ma.std(data), 3)
        progress(1, 11)
        self.median_value = np.round(np.ma.median(data), 3)
        progress(2, 11)
        self.iqr_value = (np.round(np.quantile(data, 0.25), 3), round(np.quantile(data, 0.75), 3))
        progress(3, 11)
        # generate bins
        bins = np.arange(start = self.lower_value, stop = self.upper_value + self.step_size_value, step = self.step_size_value)
        progress(4, 11)
        # generate numpy histogram data
        histogram_data = np.histogram(data, bins=bins)
        progress(5, 11)
        # determine the minimum y value and at which x this occurs
        self.min_y = np.round(np.ma.min(np.histogram(data, bins=bins)[0]), 3)
        self.min_y_val = np.round(histogram_data[1][np.where(histogram_data[0] == self.min_y)[0][0]], 3)
        progress(6, 11)
        # determine the maximum y value and at which x this occurs
        self.max_y = np.round(np.ma.max(histogram_data[0]), 3)
        self.max_y_val = np.round(histogram_data[1][np.where(histogram_data[0] == self.max_y)[0][0]], 3)
        progress(7, 11)
        # determine the minimum x (bin) value and its size
        self.min_x = np.round(histogram_data[1][0], 3)
        self.min_x_val = np.round(histogram_data[0][0], 3)
        progress(8, 11)
        # determine the maximum x (bin) value and its size
        self.max_x = np.round(histogram_data[1][-1], 3)
        self.max_x_val = np.round(histogram_data[0][-1], 3)
        progress(9, 11)
        # percent negative
        percent = np.ma.sum(data < 0)/len(data) * 100
        self.percent_negative_value = round(percent, 3)
        progress(10, 11)
        self._build_stats()

    # Commands (Callbacks)
    def __parametric(self):
        self.parametric = True
        self.non_parametric = False
        self._build_interactive_histogram()

    def __non_parametric(self):
        self.non_parametric = True
        self.parametric = False
        self._build_interactive_histogram()

    def __none(self):
        self.non_parametric = False
        self.parametric = False
        self._build_interactive_histogram()

    def __update_data(self, event):
        choice = self.drop_down_var.get()[:2]
        if choice == '1.':
            self.specs = (False, True, False)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '2.':
            self.specs = (False, True, True)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '3.':
            self.specs = (False, False, False)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '4.':
            self.specs = (False, False, True)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '5.':
            self.specs = (True, True, False)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '6.':
            self.specs = (True, True, True)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '7.':
            self.specs = (True, False, False)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '8.':
            self.specs = (True, False, True)
            self.listener._update_histogram_specs(self.specs)
        elif choice == '9.':
            data = self.listener.get_current_rec_data()
            self.update_histogram(data)
        elif choice == '10':
            data = self.listener.get_current_norm_rec_data()
            self.update_histogram(data)
        elif choice == '11':
            data = self.listener.get_current_new_data()
            self.update_histogram(data)
        elif choice == '12':
            data = self.listener.get_current_norm_new_data()
            self.update_histogram(data)
        if choice[1] != '.':
            self.spec_number = choice
        else:
            self.spec_number = choice[0]

    def __update_to_original_data(self):
        self.listener._broadcast_to_histogram()

    def __update_to_wl_data(self):
        data = self.listener.get_wl()
        self.update_histogram(data)
        
    def __update_to_idx_data(self):
        data = self.listener.get_idx()
        self.update_histogram(data)

    def __reset(self):
        self.x_lower_scale_value = None
        self.x_upper_scale_value = None
        self.y_lower_scale_value = None
        self.y_upper_scale_value = None
        self.update_histogram(self.flattened_data)

    def __info(self):
        info = self.listener.get_hist_info()
        title = "Histogram Information"
        make_info(title=title, info=info)

    def __update_upper_lower(self, event):
        self.upper_value = float(self.upper_input.get())
        self.lower_value = float(self.lower_input.get())
        self._calc_stats()

    def __update_scales(self, event):
        self.x_upper_scale_value = float(self.x_upper_scale_input.get())
        self.y_upper_scale_value = float(self.y_upper_scale_input.get())
        self.x_lower_scale_value = float(self.x_lower_scale_input.get())
        self.y_lower_scale_value = float(self.y_lower_scale_input.get())
        self.step_size_value = float(self.step_size_input.get())
        self._build_interactive_histogram()

    def __pop_up_image(self, event):
        make_popup_image(self.interactive_histogram_graph)

    def __update_save_with_scale_check_status(self, event):
        value = self.get_save_checkbox_value()
        self.listener.update_saved(HISTOGRAM_IMAGE, value)

    def __update_save_wo_scale_check_status(self, event):
        value = self.get_save_wo_scale_checkbox_value()
        self.listener.update_saved(HISTOGRAM_IMAGE_WO_SCALE, value)

    def __update_save_as_excel_check_status(self, event):
        value = self.get_save_as_excel_checkbox_value()
        self.listener.update_saved(HISTOGRAM_EXCEL, value)