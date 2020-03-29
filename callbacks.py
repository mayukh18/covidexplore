from bokeh.models import CustomJS

def get_callback(identifier, args=None):

    if identifier == 'NO2_slider':
        return CustomJS(args=dict(source=args[0], sc=args[1]), code="""
                var f = slider.value;
                console.log("map",Object.keys(map.document._all_models)[0]);
                var idx = Object.keys(map.document._all_models)[0];
                console.log("hello", f, map);
                for (var i = 0; i < map.document._all_models[idx].data['week'].length; i++){
                    if (map.document._all_models[idx].data['week'][i] != -1){
                        for (var j = 0; j<source.data['week'].length; j++){
                            if (source.data['week'][j] == f && source.data['country'][j] == map.document._all_models[idx].data['country'][i]){
                                map.document._all_models[idx].data['NO2'][i] = source.data['NO2'][j];
                                break;
                            }
                        }
                    }
                    map.document._all_models[idx].data['week'][i] = f;
                }
                console.log("hello2", sc);
                map.document._all_models[idx].change.emit();
                sc.change.emit();
            """)

    elif identifier == 'PM25_slider':
        return CustomJS(args=dict(source=args[0], sc=args[1]), code="""
                var f = slider.value;
                console.log("source", source);
                var idx = Object.keys(map.document._all_models)[0];
                console.log("hello", f, map.document._all_models[idx].data['week'].length, source);
                for (var i = 0; i < map.document._all_models[idx].data['week'].length; i++){
                    if (map.document._all_models[idx].data['week'][i] != -1){
                        for (var j = 0; j<source.data['week'].length; j++){
                            if (source.data['week'][j] == f && source.data['country'][j] == map.document._all_models[idx].data['country'][i]){
                                map.document._all_models[idx].data['PM25'][i] = source.data['PM25'][j];
                                break;
                            }
                        }
                    }
                    map.document._all_models[idx].data['week'][i] = f;
                }
                console.log("hello2", sc);
                map.document._all_models[idx].change.emit();
                sc.change.emit();
            """)

    elif identifier == 'climate_play_button':
        return CustomJS(code="""
                if (button.label == '► Play'){
                    button.label = '❚❚ Pause';
                    intervalID = setInterval(function(){
                    var year = slider.value + 1;
                    if (year > 13){
                        year = 1;
                    }
                    slider.value = year;
                    }, 500);
                }
                else{
                    clearInterval(intervalID);
                    button.label = '► Play';
                }
            """)

    elif identifier == 'hover_cursor':
        return CustomJS(code="""
                if((Bokeh.grabbing == 'undefined') || !Bokeh.grabbing) {
                    var elm = document.getElementsByClassName('bk-canvas-events')[0];
                    if (cb_data.index.indices.length > 0)
                        elm.style.cursor = 'pointer' 
                    else
                        elm.style.cursor = 'grab'
                }
            """)

    elif identifier == 'dark_slider':
        return CustomJS(args=dict(source=args[0], sc=args[1]), code="""
                var f = slider.value;
                console.log("map",Object.keys(map.document._all_models)[0]);
                var idx = Object.keys(map.document._all_models)[0];
                console.log("hello", f, map.document._all_models[idx].data['week'].length, source);
                for (var i = 0; i < map.document._all_models[idx].data['week'].length; i++){
                    if (map.document._all_models[idx].data['week'][i] != -1){
                        for (var j = 0; j<source.data['week'].length; j++){
                            if (source.data['week'][j] == f && source.data['country'][j] == map.document._all_models[idx].data['country'][i]){
                                map.document._all_models[idx].data['count'][i] = source.data['count'][j];
                                map.document._all_models[idx].data['count_true'][i] = source.data['count_true'][j];
                                break;
                            }
                        }
                    }
                    map.document._all_models[idx].data['week'][i] = f;
                }
                console.log("hello2", sc);
                map.document._all_models[idx].change.emit();
                sc.change.emit();
            """)

    elif identifier == 'dark_play_button':
        return CustomJS(code="""
                if (button.label == '► Play'){
                    button.label = '❚❚ Pause';
                    intervalID = setInterval(function(){
                    var week = slider.value;
                    console.log('play_button', week);
                    if (week > 13){
                        week = 4;
                    }
                    slider.value = week + 1;
                    }, 500);
                }
                else{
                    clearInterval(intervalID);
                    button.label = '► Play';
                }
            """)