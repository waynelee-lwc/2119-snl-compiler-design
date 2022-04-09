$('#code').on('keydown', function(e) {
    if (e.key == 'Tab') {
      e.preventDefault();
      var start = this.selectionStart;
      var end = this.selectionEnd;
  
      // set textarea value to: text before caret + tab + text after caret
      this.value = this.value.substring(0, start) +
        "\t" + this.value.substring(end);
  
      // put caret at right position again
      this.selectionStart =
        this.selectionEnd = start + 1;
    }
  });

$('#code').on('input',function(e){
    resetLines()
})


//分析程序按钮
$('.btn-analysis').on('click',function(){
    let program = $('#code').val()

    $.ajax({
        // url:'http://60.205.211.19:3008/compile',
        url:'http://localhost:3008/compile',
        type:'post',
        headers:{
            'Content-Type':'application/json'
        },
        data:JSON.stringify({
            src:program
        }),
        success:function(res){
            lexErrList = JSON.parse(res.lex_err)
            synErrList = JSON.parse(res.syn_err)

            if(!resetErrorPanel(lexErrList,synErrList[0],null)){
                $('html, body').animate({scrollTop: $('.errors').offset().top}, 300) 
                return
            }

            tokenList = JSON.parse(res.tokens)
            tree = res.tree
            resetTokenList(tokenList)
            resetSyntaxTree(tree)
            
            $('html, body').animate({scrollTop: $('.errors').offset().top}, 300) 
        }
    })
})

//格式化程序按钮
$('.btn-format').on('click',function(){
    let program = $('#code').val()

    $.ajax({
        // url:'http://60.205.211.19:3008/compile',
        url:'http://localhost:3008/compile',
        type:'post',
        headers:{
            'Content-Type':'application/json'
        },
        data:JSON.stringify({
            src:program
        }),
    
        success:function(res){
            lexErrList = JSON.parse(res.lex_err)
            synErrList = JSON.parse(res.syn_err)

            if(!resetErrorPanel(lexErrList,synErrList[0],null)){
                $('html, body').animate({scrollTop: $('.errors').offset().top}, 100) 
                return
            }
            gene = res.gene
            resetCode(gene)
        }
    })
})

//重置按钮
$('.btn-reset').on('click',function(){
    if(!confirm('是否清空当前内容？')){
        return
    }
    resetCode('')
    resetTokenList([])
    resetSyntaxTree('')
})

function resetErrorPanel(lexErr,synErr,semErr){
    //清除errs类
    $('.lex-errs').removeClass('errs')
    $('.syn-errs').removeClass('errs')
    $('.sem-errs').removeClass('errs')
    //清空展示列表
    $('.lex-err-list').empty()
    $('.syn-err-list').text('')
    //重置文字
    $('.lex-errs h3').text('Great!No lexical error!')
    $('.syn-errs h3').text('Great!No Syntax error!')
    $('.sem-errs h3').text('Great!No Sematic error!')

    let flag = true
    //词法分析错误
    if(lexErr && lexErr.length > 0){
        $('.lex-errs').addClass('errs')
        $('.lex-errs h3').text('Ops! lexical errros!')
        for(let err of lexErr){
            $('.lex-err-list').append(
                $(`<div class="lex-error">
                        <div class="lex-error-pos">${err.line},${err.col}</div>
                        <div class="lex-error-detail">${err.err}</div>
                    </div>`)
            )
        }
        flag = false
    }

    //语法分析错误
    if(synErr && synErr != ''){
        $('.syn-errs').addClass('errs')
        $('.syn-errs h3').text('Ops! syntax errors!')
        $('.syn-err-list').text(synErr)
        flag = false
    }
    return flag
}

function resetCode(program){
    $('.code').val(program)
    resetLines()
}

function resetSyntaxTree(tree){
    $('.syntax-tree>.tree').val(tree)
}

function resetTokenList(tokenList){
    $('.tokenlist').empty()
    for(let i = 0;i < tokenList.length;i++){
        let token = tokenList[i]
        $('.tokenlist').append(
            $(`<div class="token">
                    <div class="idx">${i+1}</div>
                    <div class="type">${token.type}</div>
                    <div class="name">${token.name}</div>
                    <div class="line">${token.line}</div>
                    <div class="col">${token.col}</div>
                </div>`)
        )
    }
}

function resetLines(){
    let program = $('.code').val()
    let lines = 1
    for(let i of program){
        if(i == '\n'){
            lines++
        }
    }
    lines = Math.max(lines,20)
    $('.lines').empty()
    for(let i = 1;i <= lines;i++){
        $('.lines').append(
            $(`<div>${i}</div>`)
        )
    }
    $('.code').css({height:`${lines*1.5+0.125}rem`})
}

resetLines(20)