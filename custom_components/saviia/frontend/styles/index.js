import { alertStyle } from "./alert_style";
import { formStyle } from "./form_style";
import { generalStyle } from "./general_style";
import { modalStyle } from "./modal_style";
import { tableStyle } from "./table_style";

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