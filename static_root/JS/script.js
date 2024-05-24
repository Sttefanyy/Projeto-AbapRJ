// Carrosel
var radio = document.querySelector('.manual-btn')
var cont = 1

document.getElementById('radio1').checked = true

setInterval(() => {
    proximaImg()
}, 5000)

function proximaImg(){
    cont++

    if(cont > 4){
        cont = 1
    }

    document.getElementById('radio' + cont).checked = true
}

//Sobre o projeto
var botao = document.getElementById('read_button')

botao.addEventListener('click', function(){
    var card = document.querySelector('.sobreOProjeto')
    var imagem = document.getElementById('iconeSeta')
    var texto = document.getElementById('descritivo')
    card.classList.toggle('active')

    if(imagem.src.includes('imagens/SetaParaBaixo.svg')){
        imagem.src = 'imagens/SetaParaCima.svg'
        imagem.alt = 'Seta para cima'
    } else {
        imagem.src = 'imagens/SetaParaBaixo.svg'
        imagem.alt = 'Seta para baixo'
    }

    if(texto.textContent == 'Leia mais'){
        texto.textContent = 'Leia menos'
    } else {
        texto.textContent = 'Leia mais'
    }
})


//Crianças
var btn1 = document.getElementById('imgCriancaPQ1')
var btn2 = document.getElementById('imgCriancaPQ2')
var btn3 = document.getElementById('imgCriancaPQ3')
var btn4 = document.getElementById('imgCriancaPQ4')

function tracaImagem1(){
    var imagemGrande = document.getElementById('imagemCriancaGrande')

    imagemGrande.src = 'imagens/menu01.jpg'
}

function tracaImagem2(){
    var imagemGrande = document.getElementById('imagemCriancaGrande')

    imagemGrande.src = 'imagens/menu02.jpg'
}

function tracaImagem3(){
    var imagemGrande = document.getElementById('imagemCriancaGrande')

    imagemGrande.src = 'imagens/menu03.jpg'
}

function tracaImagem4(){
    var imagemGrande = document.getElementById('imagemCriancaGrande')

    imagemGrande.src = 'imagens/menu04.jpg'
}