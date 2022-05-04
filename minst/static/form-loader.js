"use strict";

/* DRG */
window.minst = {

    inicialize: function () {
        minst.catchFormSubmit();
    },

    catchFormSubmit: function () {
        $(document).on('submit', '#post-form', function (e) {
            e.preventDefault();
            minst.myRequestAndDo('POST', '/prediction', minst.readFormDatas(), minst.renderStimation);
        });
    },

    readFormDatas: function () {
        return {
            img: $('#img').val(), csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), action: 'POST'
        }
    },

    renderStimation: function (json) {
        var predictions = minst.createPredictionsDataParagraph(json.prediction_models, 'col-md-4')
        var image = minst.createImage(json, 'col-md-8')
        $("#response").prepend(minst.createDataStructure(predictions, image))
    },

    createPredictionsDataParagraph: function (json, spaceClass) {
        var prediction_models = ""
        if (json != null) {
            Object.keys(json).forEach(function (key) {
                prediction_models = prediction_models + "<p class='" + spaceClass + "'>" + key + ": " + json[key] + "</p>"
            });
        } else {
            prediction_models = "Predicciones no disponibles"
        }
        return prediction_models
    },

    createImage: function (json, spaceClass) {
        var image_div = ""
        if (json != null) {
            image_div = "<img class='limited col-md-4' src='/static/tmp/" + json['img_name'] + "'/>"
        } else {
            image_div = "Imagen no disponible"
        }
        return image_div
    },

    createDataStructure: function (predictions, image) {
        return '<div class="col-md-6">' +
            '<div class="no-gutters grey border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative p-2">' +
            '<a href="#" onclick="$(this).parent().remove();return false;" class="close">&times;</a>' +
            '<h4 class="mb-2 mt-3">Predicciones de los modelos</h4>' +
            '<div class="ml-1 col-md-12 border row">' +
            image +
            predictions +
            '</div>' +
            '</div>' +
            '</div>';
    },

    myRequestAndDo: function (pType, pUrl, pData, pOkeyDo) {
        $.ajax({
            type: pType,
            url: pUrl,
            // data: pData,
            contentType: false,
            cache: false,
            processData:false,
            data: new FormData($('#post-form')[0]),
            success: function (json) {
                pOkeyDo(json);
            },
            error: function (xhr, errmsg, err) {
                $('#error').html("<div class='alert alert-danger' data-alert>Oops! We have encountered an error: <p>"
                    + xhr.status + "</p> <a href='#' onclick='$(this).parent().remove()' class='close'>&times;</a></div>");
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}

$(document).ready(minst.inicialize);