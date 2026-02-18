import { css } from "lit";

export const formStyle = css`

form {
    width: 90vw;
    max-width: 500px;
    margin: 0 auto;
    padding: 2em 1em;
}

fieldset {
    border: none;
    padding: 1.5rem 0;
    border-bottom: 1px solid #e0e0e0;
}

fieldset:last-of-type {
    margin-top: 1rem;
    border-bottom: none;
}

label {
    display: block;
    margin: 0.5rem 0;
    color: #212121;
}

label p {
    text-align: left;
}

i {
    font-style: normal;
    font-size: small;
    color: #a7a7a7;
}

input,
textarea,
select,
select {
    margin: 8px 0 0 0;
    width: 100%;
    min-height: 2.5em;
    box-sizing: border-box;
}

textarea,
select {
    max-width: 100%;
    border-radius: 0.5rem;
    resize: vertical;
}

input,
textarea,
select {
    background-color: #ffffff;
    border: 1px solid #bdbdbd;
    padding: 0.5rem;
    color: #212121;
    border-radius: 0.5rem;
}

input {
    padding: 0.5rem;
}

input[type="submit"] {
    display: block;
    width: 90%;
    max-width: 300px;
    margin: 2em auto;
    height: 2.5em;
    font-size: 1rem;
    background-color: #03a9f4;
    border: none;
    cursor: pointer;
    color: #ffffff;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: background-color 0.2s;
}

input[type="submit"]:hover {
    background-color: #0288d1;
}

#dropzone {
    border: 2px dashed #0056b3;
    border-radius: 8px;
    padding: 30px;
    text-align: center;
    cursor: pointer;
    background-color: rgba(0, 123, 255, 0.05);
    transition: all 0.3s ease;
    margin: 15px 0;
    }

#dropzone:hover {
    background-color: rgba(0, 123, 255, 0.1);
    border-color: #0056b3;
}

#dropzone.dragover {
    background-color: rgba(0, 123, 255, 0.2);
    border-color: #0056b3;
    box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
}

#preview {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 15px;
}

.preview-img-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preview-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.delete-img-btn {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 30px;
    height: 30px;
    padding: 0;
    background-color: rgba(255, 0, 0, 0.8);
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease;
}

.delete-img-btn:hover {
    background-color: rgba(255, 0, 0, 1);
}

#priority-nums {
    display: flex;
    list-style: none;
    justify-content: space-between;
    margin: 0.5rem 0 0 0;
    padding: 0.0rem 0.8rem 0.8rem 0.8rem;
    font-size: smaller;
    color: #757575;
}
`
