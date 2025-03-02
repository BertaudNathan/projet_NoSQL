
var compteur = 0;

function add_question(){
    let idstr = "question" + compteur;
    $(".form-container").append(
        `<div id="${idstr}" class="form-group">`+
        '<label for="Question">Question - Réponse ouverte - '+compteur+'</label>'+ `<button type="button" class="btn btn-danger" onclick="supprimer_question('${idstr}')">X</button>`+
        `<input form="formulaire" placeholder="Renseignez l'intitulé de la question" type="text" class="form-control" id="question" name="question${compteur}[]">`+
        '</div>');
    compteur++;
}


function setCompteur(value){
    compteur = value;
    console.log(compteur);
}

function supprimer_question(id){
    $("#"+id+'').remove();
    compteur--;
}

function add_question_multiple(){
    let idstr = "question" + compteur;
    $(".form-container").append(

        `<div id="${idstr}" class="form-group">`+
        '<label for="Question">Question - Choix multiple - '+compteur+'</label>'+ `<button type="button" class="btn btn-danger" onclick="supprimer_question('${idstr}')">X</button>`+`<button type="button" class="btn btn-danger" onclick="add_reponse_question_multiple('${compteur}')">+</button>`+
        `<input form="formulaire" placeholder="Renseignez l'intitulé de la question" type="text" class="form-control" id="${compteur}" name="questionMultiple${compteur}[]">`+

        `<div class="form-group" id="container${compteur}">`+
        '<label for="reponse">Réponse</label>'+
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse${compteur}[]">`+
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse${compteur}[]">`+
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse${compteur}[]">`+
        '</div>'+
        '</div>');
    compteur++;
}

function add_reponse_question_multiple(id){
    $(`#container${id}`).append(
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse${id}[]">`
        );
}


$().ready(function(){
    $(".add_question").click(function(){
    add_question();
    });
    $(".add_question_multiple").click(function(){
        add_question_multiple();
    });
     $(".add_reponse_question_multiple").click(function(e){
        add_reponse_question_multiple(e.id);
    });
});
