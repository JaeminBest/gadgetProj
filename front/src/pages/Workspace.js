import React, { Component } from 'react';
import {SketchField, Tools} from 'components/react-sketch';
import styles from './Workspace.scss';
import classNames from 'classnames';
import * as api from '../lib/api';

const cx = classNames.bind(styles);

class Workspace extends Component {
    constructor(props){
        super(props);
        console.log("constructor");
        this.state = {
            loading: false,
            download_URL: null,
            
            fixed_URL: null,
    
            zoom_factor: 1,
    
            width: 905,
            height: 14,
            
            user_id: 60000,
            org_id: 15000,
                
            upload_path: 'admin/save_edited_image',
    
        };
    }
    

    getImageSize = async (dataUrl) => {
        try {
            const img = await api.imageLoader(dataUrl);

            console.log("Get image size start")
            this.setState({
                width: img.width,
                height: img.height
            })
            console.log("Get image size complete");
        }
        catch (e) {
            console.log(e);
        }
    }

    getImage = async (image_route, org_id) => {
        try {
            const response = await api.getImage(image_route, org_id);
            console.log(response);
            const dataUrl = `data:image/png; base64, ${response.data.photo}`;
            this.getImageSize(dataUrl);

            this.setState({
                org_id: response.data.id,
                download_URL: dataUrl,
                fixed_URL: dataUrl,
                zoom_factor: 1
                
            });
            console.log("Setstate end")
            this._sketch.setBackgroundFromDataUrl(this.state.fixed_URL);
        }

        catch(e) {
            console.log(e);
        }
    
    }

    postImage = async (user_id, org_id, upload_string, upload_route) => {
        //const today = Date();
        const today = "2019-03-06 12:00:00";
        //console.log(today);

        try {
            const response = await api.postImage(user_id, org_id, today, upload_string, upload_route);
            console.log("response :",response);
            
            let win = window.open();
            win.document.write('<iframe src="data:image/png;base64,' + upload_string + '" frameborder="0" style="border:0; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%;" allowfullscreen></iframe>')
        }

        catch(e) {
          console.log(e);
        }

    }

    handleZoom = async (zoomFactor) => {
        const {download_URL} = this.state;
        const fixed_URL = await api.imageFixer(download_URL, zoomFactor);
        
        this.setState({
            zoom_factor: zoomFactor,
            fixed_URL: fixed_URL
        });

    }

    handleReduce_2 = () => {
        this.handleZoom(0.5);
        console.log("x0.5")
    }
    handleZoom_1 = () => {
        const {download_URL} = this.state;
        this.setState({
            zoom_factor: 1,
            fixed_URL: download_URL
        });
        console.log("x1")
    }
    handleZoom_2 = () => {
        this.handleZoom(2);
        console.log("x2")
    }
    handleZoom_4 = () => {
        this.handleZoom(4);
        console.log("x4")
    }
        
    handleReset = () => {
        this._sketch.clear();
        this.handleZoom(1);

    }

    handleUpload = async() => {
       const {download_URL} = this.state;
        
        try {
            if (this.state.zoom_factor !== 1) {
                this.setState({
                    zoom_factor: 1,
                    fixed_URL: download_URL
                });
            }

            const response = await this._sketch.setBackgroundFromDataUrl(download_URL);
            console.log(response);

        } catch(e) {
            console.log(e);
        }

        const upload_url = this._sketch.toDataURL("image/png");

        let string_list = upload_url.split(',');
        let upload_string = string_list[1];

        const { user_id, org_id, upload_path } = this.state;

        this.postImage(user_id, org_id, upload_string, upload_path);
        
    }

    componentDidMount() {
        console.log("componentDidMount");
        this.getImage('admin/show_one_image', 15000);
        
    }

    
    shouldComponentUpdate() {
        console.log("shouldComponentUpdate");
        return true;
        //return this.state !== this.prevState;
    }
    
    /*
    componentWillUpdate() {
        
    }

    */
    componentDidUpdate = () => {
        console.log("componentDidUpdate");
        this._sketch.setBackgroundFromDataUrl(this.state.fixed_URL);
        //console.log(this.state.fixed_URL === this.state.download_URL)
    }

    render () {
        console.log("render");
        return (
        <div className="fragment">

            <div className = "instructions brown lighten-5">
              Please mark the <b>most prominent defect </b>in the image.<br/>
                When your job is done, <br/>
                please click the <b>"Submit"</b> button to create a new labeling function!<br/>
            </div>
            <div className = "sketch-box brown lighten-5">

                    <SketchField className = "sketch-field"
                                 ref={c => (this._sketch = c)}
                                 width={this.state.width * this.state.zoom_factor}
                                 height={this.state.height * this.state.zoom_factor} 
                                 tool={Tools.Pencil} 
                                 lineColor='red'
                                 lineWidth={3 * this.state.zoom_factor}/>

            </div>
            <div className = {cx("buttons")}>   
                <button className={cx("reset-button", "btn", "$oc-gray-9")} onClick = {this.handleReset}>Reset</button>
                <button className={cx("x05-button", "waves-effect", "waves-light", "btn", "$oc-gray-9")} onClick = {this.handleReduce_2}>X0.5</button>
                <button className={cx("x1-button", "waves-effect", "waves-light", "btn", "$oc-gray-9")} onClick = {this.handleZoom_1}>X1</button>
                <button className={cx("x2-button", "waves-effect", "waves-light", "btn", "$oc-gray-9")} onClick = {this.handleZoom_2}>X2</button>
                <button className={cx("x4-button", "waves-effect", "waves-light", "btn", "$oc-gray-9")} onClick = {this.handleZoom_4}>X4</button>
                <button className={cx("submit-button", "btn", "waves-effect", "waves-light", "$oc-gray-9")} onClick = {this.handleUpload} type="submit" name="action">
                    Submit<i className={cx("material-icons", "right")}>send</i>
                </button>
            </div>

        </div>
                
        );
    }
}

export default Workspace;
