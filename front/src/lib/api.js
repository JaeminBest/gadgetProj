import axios from 'axios';

export function getImage(image_route, org_id) {
    return axios.get(`http://localhost:8000/${image_route}`, {
        params: {
            id : `${org_id}`
        }
    });
}

export function postImage(user_id, org_id, date, upload_file, upload_route) {
    let body = {
        user_id: user_id,
        org_id: org_id,
        date_edited: date,
        photo: upload_file
    }
    return axios.post(`http://localhost:8000/${upload_route}`, body);
}

/*
{
    user_id: user_id,
    org_id: org_id,
    upload_file: `${upload_file}`
}
*/


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
            
            /*
            let win = window.open();
            win.document.write('<iframe src="data:image/png;base64,' + ctxUrl + '" frameborder="0" style="border:0; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%;" allowfullscreen></iframe>')

            */

            //console.log("context url : ",ctxUrl);
            resolve(ctxUrl);
            
        }
        img.src = src;
    })

}
