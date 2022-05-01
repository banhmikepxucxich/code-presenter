# DearPyGui with pywebview

import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Code Presenter', width=600, height=600)

with dpg.window(tag='Primary Window'):
    dpg.add_text('CodePresenter owo')
    dpg.add_button(label='save')
    dpg.add_input_text(label='string', default_value='Quick brown fox')
    dpg.add_slider_float(label='float', default_value=0.273, max_value=1)

    # send help wheres webview

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()