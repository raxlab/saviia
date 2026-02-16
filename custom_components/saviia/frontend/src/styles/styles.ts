import { alertStyle } from "./alert_style";
import { formStyle } from "./form_style";
import { generalStyle } from "./general_style";
import { modalStyle } from "./modal_style";
import { tableStyle } from "./table_style";

export class Styles {
    private stylesList: Record<string, any> = {
        'alert': alertStyle,
        'form': formStyle,
        'general': generalStyle,
        'modal': modalStyle,
        'table': tableStyle,
    }
    public getStyles(styles: Array<string>) {
        return styles
            .filter(style => style in this.stylesList)
            .map(style => this.stylesList[style]);
    }

    public getStyle(style: string) {
        return this.stylesList[style]
    }
}