import { CONFIG } from "./new_task_constants.js";
let hass = null;

const dropzone = document.getElementById("dropzone");
const imageInput = document.getElementById("image-input");
const preview = document.getElementById("preview");

let imagesBase64 = [];
dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
});
dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
});
dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    handleFiles(e.dataTransfer.files);
});
dropzone.addEventListener("click", () => {
    imageInput.click();
});
imageInput.addEventListener("change", (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    [...files].forEach(file => {
        if (!file.type.startsWith("image/")) return;
        if (!CONFIG.ACCEPTED_IMAGE_TYPES.includes(file.type)) {
            alert("Tipo de archivo no soportado. Por favor, sube una imagen JPEG, PNG o GIF.");
            return;
        }
        const reader = new FileReader();
        reader.onload = () => {
            const imgObj = {
                name: file.name,
                type: file.type,
                data: reader.result.split(",")[1]
            };
            imagesBase64.push(imgObj);
            const wrapper = document.createElement("div");
            wrapper.className = "preview-img-wrapper";
            const img = document.createElement("img");
            img.src = reader.result;
            wrapper.appendChild(img);
            const delBtn = document.createElement("button");
            delBtn.type = "button";
            delBtn.className = "delete-img-btn";
            delBtn.textContent = "X";
            delBtn.onclick = () => {
                const idx = imagesBase64.indexOf(imgObj);
                if (idx > -1) imagesBase64.splice(idx, 1);
                alert("Imagen eliminada ✅");
                wrapper.remove();
            };
            wrapper.appendChild(delBtn);
            preview.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
}

document.getElementById("survey-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("submit");
    btn.disabled = true;
    
    if (!hass) {
        alert("Error: Home Assistant connection not available");
        btn.disabled = false;
        return;
    }

    const title = document.getElementById("task-title").value;
    const details = document.getElementById("details").value
        ? document.getElementById("details").value
        : "Sin descripción";
    const assignee = document.getElementById("author").value
        ? document.getElementById("author").value
        : "No asignada";
    const category = document.getElementById("categ").value
        ? document.getElementById("categ").value
        : "Sin categoría";
    const deadline = document.getElementById("deadline").value
        ? document.getElementById("deadline").value
        : "";
    const periodicity = document.getElementById("periodicity").value
        ? document.getElementById("periodicity").value
        : "Sin periodicidad";
    const periodicityNum = document.getElementById("periodicity-number").value
        ? parseInt(document.getElementById("periodicity-number").value)
        : 1;
    const priority = document.getElementById("priority").value
        ? document.getElementById("priority").value
        : "Baja";

    // Validate title
    if (!title) {
        alert("Por favor, ingresa un título para la tarea.");
        btn.disabled = false;
        return;
    }

    // Validate periodicity
    if (periodicity !== "Sin periodicidad" && periodicityNum === 0) {
        alert("No definiste un número válido para la periodicidad.");
        btn.disabled = false;
        return;
    }

    try {
        // Prepare service call data
        const serviceData = {
            title,
            details,
            assignee,
            category,
            deadline,
            periodicity,
            periodicity_num: periodicityNum,
            priority,
            images: imagesBase64
        };

        const result = await hass.callService(
            "saviia",
            "create_task",
            serviceData,
            { returnResponse: true }
        );

        if (!result?.return_value?.success) {
            alert(`Error: ${result?.return_value?.error || "Unknown error"}`);
        } else {
            alert(result.return_value.message || "Tarea creada con éxito ✅");
            document.getElementById("survey-form").reset();
            imagesBase64 = [];
            while (preview.firstChild) {
                preview.removeChild(preview.firstChild);
            }
        }
    } catch (err) {
        console.error(err);
        alert("Hubo un error al crear la tarea. Por favor, inténtalo de nuevo.");
    } finally {
        btn.disabled = false;
    }
});
