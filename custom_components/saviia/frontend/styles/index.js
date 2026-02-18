import { alertStyle } from "./alert_style.js";
import { formStyle } from "./form_style.js";
import { generalStyle } from "./general_style.js";
import { modalStyle } from "./modal_style.js";
import { tableStyle } from "./table_style.js";

export class Styles {
    constructor() {
        this.stylesList = {
            'alert': alertStyle,
            'form': formStyle,
            'general': generalStyle,
            'modal': modalStyle,
            'table': tableStyle,
        };
    }

    getStyles(styles) {
        return styles
            .filter(style => style in this.stylesList)
            .map(style => this.stylesList[style]);
    }

    getStyle(style) {
        return this.stylesList[style];
    }
}