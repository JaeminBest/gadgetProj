import axios from 'axios';

export function getImage(image_route, org_id) {
    return axios.get(`http://localhost:8000/${image_route}`, {
        params: {
            id : `${org_id}`
        }
    });
}

export function postImage(user_id, org_id, uploadFile, upload_route) {
    return axios.post(`http://localhost:8000/${upload_route}`, {
        user_id: `${user_id}`,
        org_id: `${org_id}`,
        uploadFile: `${uploadFile}`
    });
}

export function postImageImm(image_body) {
    return axios.post(`admin/request_checking`, image_body);
}