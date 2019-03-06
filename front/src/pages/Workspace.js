import React, { Component } from 'react';

import {SketchField, Tools} from 'components/react-sketch';

import * as api from '../lib/api';

class Workspace extends Component {
    state = {
        loading: false,
        sampleFile: null,
        uploadFile: null,
        width: 2702,
        height: 162,
        user_id: 1,
        org_id: 15000,
        upload_path: 'admin/request_checking',

    };

    //_sketch = React.createRef();

    getImage = async (image_route, org_id) => {
        try {
            const response = await api.getImage(image_route, org_id);
            console.log(response);

            const dataUrl = `data:image/png; base64, ${response.data.photo}`;
            //console.log('data URL: ', dataUrl);

            this.setState ({
                sampleFile: dataUrl
            });

            console.log('sketch :', this._sketch);
            this.handleReset();
            //this._sketch.setBackgroundFromDataUrl(this.state.sampleFile);

            /*
            this.setState({
            sampleFile: response.data.photo
            })
            */

        }

        catch(e) {
            console.log(e);
        }
    
    }

    postImage = async (user_id, org_id, upload_file, upload_route) => {
        try {
          const response = await api.postImage(user_id, org_id, upload_file, upload_route);
          console.log(response);
          let win = window.open();
          win.document.write('<iframe src="' + upload_file + '" frameborder="0" style="border:0; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%;" allowfullscreen></iframe>')
        }

        catch(e) {
          console.log(e);
        }

    }

    
    handleReset = () => {
        this._sketch.clear();
        this._sketch.setBackgroundFromDataUrl(this.state.sampleFile, {stretched: true});
    }

    handleUpload = () => {
        /*
        this.setState({
            uploadFile: this._sketch.toDataURL()
        });
        */
        const url_data = this._sketch.toDataURL("image/png");
        
        const { user_id, org_id, upload_path } = this.state;
        this.postImage(user_id, org_id, url_data, upload_path);
        
    }

    componentDidMount() {
        this.getImage('admin/show_one_image', this.state.org_id);
        
    }

    shouldComponentUpdate() {
        return false;
    }

    componentWillUpdate() {
        
    }

    render () {
        
        return (
            <div>
                <SketchField ref={c => (this._sketch = c)}
                             width={this.state.width}
                             height={this.state.height} 
                             tool={Tools.Pencil} 
                             lineColor='red'
                             lineWidth={3}/>
                <button onClick = {this.handleReset}>Reset</button>
                <p align="right">
                <button onClick = {this.handleUpload}
                class="btn waves-effect waves-light" type="submit" name="action">Submit
                <i class="material-icons right">send</i>
                </button>
                </p>
            </div>
        );
    }
}

export default Workspace;
