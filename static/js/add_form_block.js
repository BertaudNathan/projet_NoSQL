
var compteur = 0;

function add_question(){
    let idstr = "question" + compteur;
    $(".form-container").append(
        `<div id="${idstr}" class="form-group">`+
        '<label for="Question">Question - Réponse ouverte - '+compteur+'</label>'+ `<button type="button" class="btn btn-danger" onclick="supprimer_question('${idstr}')">X</button>`+
        `<input form="formulaire" placeholder="Renseignez l'intitulé de la question" type="text" class="form-control" id="question" name="question[]">`+
        '</div>');
    compteur++;
}


function supprimer_question(id){
    $("#"+id+'').remove();
    compteur--;
}

function add_question_multiple(){
    let idstr = "question" + compteur;
    $(".form-container").append(

        `<div id="${idstr}" class="form-group">`+
        '<label for="Question">Question - Choix multiple - '+compteur+'</label>'+ `<button type="button" class="btn btn-danger" onclick="supprimer_question('${idstr}')">X</button>`+
        `<input form="formulaire" placeholder="Renseignez l'intitulé de la question" type="text" class="form-control" id="question" name="question[]">`+

        '<div class="form-group">'+
        '<label for="reponse">Réponse</label>'+
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse[]">`+
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse[]">`+
        `<input form="formulaire" placeholder="Renseignez la réponse" type="text" class="form-control" id="reponse" name="reponse[]">`+
        '</div>'+
        '</div>');
    compteur++;
}


$().ready(function(){
    $(".add_question").click(function(){
    add_question();
    });
    $(".add_question_multiple").click(function(){
        add_question_multiple();
    });
});
