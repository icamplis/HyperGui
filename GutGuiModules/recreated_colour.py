from GutGuiModules.utility import *

class RecColour:
    def __init__(self, recreated_color_frame):
        self.root = recreated_color_frame

        self.sto2_button = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value = IntVar()

        self.nir_button = None
        self.nir_checkbox = None
        self.nir_checkbox_value = IntVar()

        self.thi_button = None
        self.thi_checkbox = None
        self.thi_checkbox_value = IntVar()

        self.twi_button = None
        self.twi_checkbox = None
        self.twi_checkbox_value = IntVar()

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()

        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = IntVar()

        self.upper_scale_text = None
        self.lower_scale_text = None
        self.upper_scale_input = None
        self.lower_scale_input = None

        self.displayed_image_mode = STO2  # STO2 by default
        self.recreated_image = None

        self._init_widget()

    def get_sto2_checkbox_value(self):
        return self.sto2_checkbox_value

    def get_nir_checkbox_value(self):
        return self.nir_checkbox_value

    def get_thi_checkbox_value(self):
        return self.thi_checkbox_value

    def get_twi_checkbox_value(self):
        return self.twi_checkbox_value

    def get_save_checkbox_value(self):
        return self.save_checkbox_value

    def get_save_wo_scale_checkbox_value(self):
        return self.save_wo_scale_checkbox_value

    def get_upper_scale_value(self):
        return self.upper_scale_input.get()

    def get_lower_scale_value(self):
        return self.lower_scale_input.get()

    # Helper
    def _init_widget(self):
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_save()
        self._build_save_wo_scale()
        self._build_upper_scale()
        self._build_lower_scale()
        self._build_recreated_image()

    def _build_sto2(self):
        self.st02_button = make_button(self.root, text='St02', width=4, command=self.__update_to_sto2, row=1, column=0, inner_pady=5, 
            outer_padx=(15, 0))
        self.sto2_checkbox = make_checkbox(self.root, "", row=1, column=0, var=self.sto2_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 15))
        self.sto2_checkbox.deselect()

    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=4, command=self.__update_to_nir, row=1, column=1, inner_pady=5, outer_padx=0)
        self.nir_checkbox = make_checkbox(self.root, "", row=1, column=1, var=self.nir_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(50, 0))
        self.nir_checkbox.deselect()

    def _build_twi(self):
        self.twi_button = make_button(self.root, text="TWI", width=6, row=1, column=2, command=self.__update_to_twi, inner_padx=0, inner_pady=5, outer_padx=(5, 12))
        self.twi_checkbox = make_checkbox(self.root, "", row=1, column=2,var=self.twi_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.twi_checkbox.deselect()

    def _build_thi(self):
        self.thi_button = make_button(self.root, text="THI", row=1, column=3, command=self.__update_to_thi, inner_padx=0, inner_pady=5, width=6, outer_padx=(0, 15))
        self.thi_checkbox = make_checkbox(self.root, "", row=1, column=3, var=self.thi_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 10))
        self.thi_checkbox.deselect()

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=8, column=0, columnspan=1, outer_padx=(50, 0), outer_pady=(10, 0), inner_padx=10, inner_pady=5)
        self.save_checkbox = make_checkbox(self.root, text="", row=8, column=0,var=self.save_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 0), outer_padx=(100, 0))

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=8, column=1, columnspan=3, outer_padx=(0, 15), outer_pady=(10, 0), inner_padx=10, inner_pady=5)
        self.save_wo_scale_checkbox = make_checkbox(self.root, text="", row=8, column=3, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 0), outer_padx=(0, 30))

    def _build_upper_scale(self):
        self.upper_scale_text = make_text(self.root, content="Upper Scale End: ", row=6, column=0, columnspan=2, width=17, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), pady=(5, 0), padx=(15, 0))
        self.upper_scale_input = make_entry(self.root, row=6, column=2, width=11, pady=(5,0), padx=(0,15), columnspan=2)

    def _build_lower_scale(self):
        self.lower_scale_text = make_text(self.root, content="Lower Scale End: ", row=7, column=0, columnspan=2, width=17, bg=tkcolour_from_rgb(PASTEL_BLUE_RGB), pady=5, padx=(15, 0))
        self.lower_scale_input = make_entry(self.root, row=7, column=2, width=11, pady=5, padx=(0,15), columnspan=2)

    def _build_recreated_image(self):
        # todo
        self.recreated_image = make_label(self.root, "recreated image placeholder", row=2, column=0, rowspan=4, columnspan=4, inner_pady=50, inner_padx=50, outer_padx=15, outer_pady=(15, 10))

    # Commands (Callbacks)
    def __update_to_sto2(self):
        self.displayed_image_mode = STO2
        pass

    def __update_to_nir(self):
        self.displayed_image_mode = NIR
        pass

    def __update_to_thi(self):
        self.displayed_image_mode = THI
        pass

    def __update_to_twi(self):
        self.displayed_image_mode = TWI
        pass

    def __update_scale_upper(self):
        pass

    def __update_scale_lower(self):
        pass

    def __update_recreated_image(self, mode):
        pass

