import axios from 'axios';

export function getImage(image_route, org_id) {
    return axios.get(`http://localhost:8000/${image_route}`, {
        params: {
            id : `${org_id}`
        }
    });
}

export function postImage(user_id, org_id, upload_file, upload_route) {
    return axios.post(`http://localhost:8000/${upload_route}`, {
        user_id: `${user_id}`,
        org_id: `${org_id}`,
        upload_file: `${upload_file}`
    });
}


export function imageLoader(src) {
    return new Promise((resolve, reject) => {
        let img = new Image();
        img.onload = () => resolve(img);
        img.src = src;
    });
    
}

export function imageFixer(src, zoom_factor) {
    return new Promise((resolve, reject) => {
        let img = new Image()
        //console.log("zoom factor received: ", zoom_factor);
        //console.log(`${zoom_factor * 100}%`);
        
        img.onload = () => {
            const width = img.width * zoom_factor;
            const height = img.height * zoom_factor;
            //console.log("width x height : ", width,"x",height);
            
            const elem = document.createElement('canvas');
            elem.width = width;
            elem.height = height;
            //console.log("elem width x height : ", elem.width,"x",elem.height);
                       
            const ctx = elem.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            const ctxUrl = ctx.canvas.toDataURL();
            
            //console.log("context url : ",ctxUrl);
            resolve(ctxUrl);
            
        }
        img.src = src;
    })

}

/*
export function imageZoom(img, zoom_factor) {
    return new Promise((resolve, reject) => {
        let width = 
    });
}



/*
export function postImageImm(image_body) {
    return axios.post(`admin/request_checking`, image_body);
}
*/