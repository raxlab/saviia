import { LitElement, html } from "lit";
import { hass } from "../../../services/ha-client";
import { Styles } from "../../../styles/styles"
import { state } from "lit/decorators.js";

interface ImageBase64 {
  name: string;
  type: string;
  data: string;
}

export class CreateTask extends LitElement {
  @state()
  private images: ImageBase64[] = [];
  
  @state()
  private isSubmitting = false;
  
  private CONFIG = {
    ACCEPTED_IMAGE_TYPES: ["image/jpeg", "image/png", "image/gif"],
  };

  static styles = new Styles().getStyles(['general', 'form', 'alerts'])

  private getPeriodicity(periodicity: string, num: string) {
    if (!periodicity) return "Sin periodicidad";

    const map: Record<string, string> = {
      daily: "día(s)",
      weekly: "semana(s)",
      monthly: "mes(es)",
      yearly: "año(s)",
    };

    return `Cada ${num} ${map[periodicity] ?? ""}`;
  }

  private handleFiles(files: FileList) {
    [...files].forEach((file) => {
      if (!this.CONFIG.ACCEPTED_IMAGE_TYPES.includes(file.type)) return;

      const reader = new FileReader();

      reader.onload = () => {
        const img = {
          name: file.name,
          type: file.type,
          data: (reader.result as string).split(",")[1],
        };

        this.images = [...this.images, img];
      };

      reader.readAsDataURL(file);
    });
  }

  private deleteImage(index: number) {
    this.images = this.images.filter((_, i) => i !== index);
  }

  private onDrop(e: DragEvent) {
    e.preventDefault();
    if (e.dataTransfer?.files) this.handleFiles(e.dataTransfer.files);
  }

  private onFileInput(e: Event) {
    const input = e.target as HTMLInputElement;
    if (input.files) this.handleFiles(input.files);
  }

  private async submitTask(e: Event) {
    e.preventDefault();
    this.isSubmitting = true;

    const form = e.target as HTMLFormElement;

    const title = (form.querySelector("#task-title") as HTMLInputElement).value;
    const deadline = (form.querySelector("#deadline") as HTMLInputElement).value;
    const priority = (form.querySelector("#priority") as HTMLInputElement).value;
    const author = (form.querySelector("#author") as HTMLInputElement).value;
    const periodicity = (
      form.querySelector("#periodicity") as HTMLSelectElement
    ).value;

    const periodicityNum = (
      form.querySelector("#periodicity-number") as HTMLInputElement
    ).value;

    const details =
      (form.querySelector("#details") as HTMLTextAreaElement).value ||
      "Sin descripción";

    const category =
      (form.querySelector("#categ") as HTMLInputElement).value ||
      "Sin categoría";

    try {
      const result = await hass.callService("saviia", "create_task", {
        'title': title,
        'details': details,
        'deadline': deadline,
        'priority': priority,
        'author': author,
        'periodicity': this.getPeriodicity(periodicity, periodicityNum),
        'category': category,
        'images': this.images
      });
      console.log(result)

      this.images = [];
      form.reset();
    } catch (err) {
      console.error(err);
    } finally {
      this.isSubmitting = false;
    }
  }

  render() {
    return html`
      <h2>Crea una nueva tarea</h2>
      <p>Completa el siguiente formulario para generar una nueva tarea</p>
      <p><i>Los campos marcados con <span style="color: #03a9f4">*</span> son obligatorios.</i></p>

      <form @submit=${this.submitTask}>
        <fieldset>
          <label>
            <p>Nombre de la tarea <span style="color: #03a9f4">*</span> </p>
            <input id="task-title" required placeholder="Nombre" />
          </label>
          <label>
            <p>Fecha de ejecución de la tarea <span style="color: #03a9f4">*</span> </p>
            <i>La(s) persona(s) encargadas de esta tarea deben finalizarla antes de esta fecha.</i>
            <input id="deadline" type="date" required />
          </label>
          <label>
            <p>Prioridad <span style="color: #03a9f4">*</span> </p>
              <i>1 es la prioridad más alta y 4 la más baja</i>
            <input id="priority" type="range" min="1" max="4" />
            <ul id="priority-nums">
              <li>1</li>
              <li>2</li>
              <li>3</li>
              <li>4</li>
            </ul>
          </label>
          <label>
            <p>Persona asignada <span style="color: #03a9f4">*</span> </p>
            <i>La persona responsable de realizar esta tarea.</i>
            <input id="author" type="text" required />
          </label>
          <label>
            <p>Periodicidad</p>
            <i>Indica si esta tarea se repite en un intervalo de tiempo específico.</i>
            <select id="periodicity">
                <option value="" selected>Ninguna</option>
                <option value="daily">Diaria</option>
                <option value="weekly">Semanal</option>
                <option value="monthly">Mensual</option>
                <option value="yearly">Anual</option>
            </select>
            <br><br><i>Indica cuántas veces se repite esta tarea en el intervalo seleccionado. Por ejemplo, si el
                usuario define una repetición diaria, entonces se repetirá cada cierto número de días.</i>
            <input id="periodicity-number" type="number" min="1" placeholder="Número de periodicidad" />
          </label>
          <label>
            <p>Categoría</p>
            <i>La categoría a la que pertenece esta tarea (opcional).</i>
            <input id="categ" type="text" />
          </label>
          <label>
            <p>Detalle de la tarea</p>
            <i>Describe los detalles específicos de la tarea, ya sea para aclarar o para dar instrucciones.</i>
            <textarea id="details" rows="4"></textarea>
          </label>
        </fieldset>
        <fieldset>
          <legend>Imágenes</legend>
          <i>Arrastra imágenes aquí o haz click para seleccionarlas. Solo se pueden agregar hasta un máximo de 10 imágenes.</i>
          <div
            id="dropzone"
            @drop=${this.onDrop}
            @dragover=${(e: DragEvent) => e.preventDefault()}
            >
            Arrastra imágenes
            <input
            type="file"
            accept="image/*"
            multiple
            @change=${this.onFileInput}
            />
          </div>
          <div id="preview">
            ${this.images.map((img, i) => html`
              <div class="preview-img-wrapper">
                <img src="data:${img.type};base64,${img.data}" />
                <button
                  type="button"
                  class="delete-img-btn"
                  @click=${() => this.deleteImage(i)}
                >
                  X
                </button>
              </div>
            `)}
          </div>
        </fieldset>

        <button ?disabled=${this.isSubmitting}>
          ${this.isSubmitting ? "Enviando..." : "Enviar tarea"}
        </button>
      </form>
    `;
  }
}

customElements.define("create-task", CreateTask);
