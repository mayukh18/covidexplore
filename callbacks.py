from bokeh.models import CustomJS

def get_callback(identifier, args=None):

    if identifier == 'NO2_slider':
        return CustomJS(args=dict(source=args[0], sc=args[1]), code="""
                var f = slider.value;
                console.log("map", map);
                
                var keys = Object.keys(map.document._all_models);
                
                // finding out the index of the one with geo data among all models
                var idx = -1;
                for (var i = 0; i < keys.length; i++){
                    try{
                        if (typeof map.document._all_models[keys[i]].geojson !== 'undefined'){
                            idx = i;
                            break;
                        }
                    }
                    catch(err){
                        pass;
                    }
                }
                
                idx = keys[idx];
                console.log("idx is", idx);
                
                for (var i = 0; i < map.document._all_models[idx].data['week'].length; i++){
                    if (map.document._all_models[idx].data['week'][i] != -1){
                        for (var j = 0; j<source.data['week'].length; j++){
                            if (source.data['week'][j] == f && source.data['country'][j] == map.document._all_models[idx].data['country'][i]){
                                map.document._all_models[idx].data['NO2'][i] = source.data['NO2'][j];
                                sc.data['NO2'][i] = source.data['NO2'][j];
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
                console.log("map", map);
                
                var keys = Object.keys(map.document._all_models);
                
                // finding out the index of the one with geo data among all models
                var idx = -1;
                for (var i = 0; i < keys.length; i++){
                    try{
                        if (typeof map.document._all_models[keys[i]].geojson !== 'undefined'){
                            idx = i;
                            break;
                        }
                    }
                    catch(err){
                        pass;
                    }
                }
                
                idx = keys[idx];
                console.log("idx is", idx);
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
                    var week = slider.value + 1;
                    if (week > max_week){
                        week = 1;
                    }
                    slider.value = week;
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
                else{
                    console.log("GRABBING");
                }
            """)

    elif identifier == 'dark_slider':
        return CustomJS(args=dict(source=args[0], sc=args[1]), code="""
                var f = slider.value;
                console.log("map", map);
                
                var keys = Object.keys(map.document._all_models);
                
                // finding out the index of the one with geo data among all models
                var idx = -1;
                for (var i = 0; i < keys.length; i++){
                    try{
                        if (typeof map.document._all_models[keys[i]].geojson !== 'undefined'){
                            idx = i;
                            break;
                        }
                    }
                    catch(err){
                        pass;
                    }
                }
                
                idx = keys[idx];
                console.log("idx is", idx);
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
                    if (week > max_week){
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

    elif identifier == 'finance_slider':
        return CustomJS(args=dict(source=args[0], sc=args[1]), code="""
                var f = slider.value;
                console.log("map", map);

                var keys = Object.keys(map.document._all_models);

                // finding out the index of the one with geo data among all models
                var idx = -1;
                for (var i = 0; i < keys.length; i++){
                    try{
                        if (typeof map.document._all_models[keys[i]].geojson !== 'undefined'){
                            idx = i;
                            break;
                        }
                    }
                    catch(err){
                        pass;
                    }
                }

                idx = keys[idx];
                console.log("idx is", idx);
                for (var i = 0; i < map.document._all_models[idx].data['week'].length; i++){
                    if (map.document._all_models[idx].data['week'][i] != -1){
                        for (var j = 0; j<source.data['week'].length; j++){
                            if (source.data['week'][j] == f && source.data['country'][j] == map.document._all_models[idx].data['country'][i]){
                                map.document._all_models[idx].data['Close'][i] = source.data['Close'][j];
                                //map.document._all_models[idx].data['Close'][i] = source.data['Close'][j];
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

    elif identifier == 'finance_play_button':
        return CustomJS(code="""
                if (button.label == '► Play'){
                    button.label = '❚❚ Pause';
                    intervalID = setInterval(function(){
                    var week = slider.value;
                    console.log('play_button', week);
                    if (week > max_week){
                        week = 1;
                    }
                    slider.value = week + 1;
                    }, 500);
                }
                else{
                    clearInterval(intervalID);
                    button.label = '► Play';
                }
            """)




    elif identifier == "tap_climate":
        return CustomJS(args=dict(overall=args[0], curr=args[1]), code="""
                var idx = cb_data.source.selected.indices[0];
                var country = cb_data.source.data.country[idx]
                
                for (var i=0;i<=overall.data['index'].length;i++){
                    if (overall.data['country'][i] == country){
                        curr.data[field_name][overall.data['week'][i] - 1] = overall.data[field_name][i];
                    }
                }
                graph.change.emit();
                curr.change.emit();
            """)

    elif identifier == "tap_climate_diff":
        return CustomJS(args=dict(overall=args[0], curr=args[1]), code="""
                var idx = cb_data.source.selected.indices[0];
                var country = cb_data.source.data.country[idx]

                for (var i=0;i<=overall.data['index'].length;i++){
                    if (overall.data['country'][i] == country){
                        curr.data[field_name][overall.data['week'][i] - 5] = overall.data[field_name][i];
                    }
                }
                graph.change.emit();
                curr.change.emit();
            """)

    elif identifier == "tap_dark":
        return CustomJS(args=dict(overall=args[0], curr=args[1]), code="""
                var idx = cb_data.source.selected.indices[0];
                var country = cb_data.source.data.country[idx]

                for (var i=0;i<=overall.data['index'].length;i++){
                    if (overall.data['country'][i] == country){
                        curr.data[field_name][overall.data['week'][i] - 4] = overall.data[field_name][i];
                    }
                }
                graph.change.emit();
                curr.change.emit();
            """)

    elif identifier == "tap_finance":
        return CustomJS(args=dict(overall=args[0], curr=args[1]), code="""
                var idx = cb_data.source.selected.indices[0];
                var country = cb_data.source.data.country[idx]

                for (var i=0;i<=overall.data['index'].length;i++){
                    if (overall.data['country'][i] == country){
                        curr.data[field_name][overall.data['week'][i] - 4] = overall.data[field_name][i];
                    }
                }
                graph.change.emit();
                curr.change.emit();
            """)