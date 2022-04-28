document.getElementsByTagName('html')[0].style.fontSize = (16/1920) * window.innerWidth + "px";
window.onresize = function(){
	// console.log("当前尺寸为：" + window.innerWidth);
	document.getElementsByTagName('html')[0].style.fontSize = (16/1920) * window.innerWidth + "px";
}

var lastProgramName = ''

// var host = '60.205.211.19'
var host = 'localhost'
var port = '3008'

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
    $('.download-outputs').attr('disabled','disabled')
    let program = $('#code').val()

    $.ajax({
        // url:'http://60.205.211.19:3008/compile',
        // url:'http://localhost:3008/compile',
        url:`http://${host}:${port}/compile`,
        type:'post',
        headers:{
            'Content-Type':'application/json'
        },
        data:JSON.stringify({
            src:program
        }),
        success:function(res){
            resetResult()  //重制所有结果展示
            $('.download-outputs').removeAttr('disabled')
            lastProgramName = res.program_name

            /************************  词法分析  ***************************/
            let lexErrList = JSON.parse(res.lex_err)        //词法分析错误  
            if(lexErrList && lexErrList.length > 0){
                //词法错误，报错
                setLexErr(lexErrList)
                scrollToResult()    //结果展示
                return
            }
            let tokenList = JSON.parse(res.tokens)  //获得token序列
            resetTokenList(tokenList)             //追加token列表

            /************************  语法分析  ***************************/
            let synErrList = JSON.parse(res.syn_err)//递归下降错误
            let ll1ErrList = res.syn_ll1_err        //ll1错误
            
            console.log(synErrList)
            if(synErrList[0] != ''){
                //语法错误
                setSynErr(synErrList,ll1ErrList)
                scrollToResult()
                return
            }

            let rdtree     = res.tree                       //递归下降语法树
            let ll1tree    = res.treell1                    //ll1语法树
            resetSyntaxTree(rdtree,ll1tree)
            
            /************************  语义分析  ***************************/
            let semErr = JSON.parse(res.semerr)         //语义分析错误
            let sem = JSON.parse(res.sem)               //

            resetSemList(sem)
            setSemErr(semErr)
            scrollToResult()
        }
    })
})

//格式化程序按钮
$('.btn-format').on('click',function(){
    $('.download-outputs').attr('disabled','disabled')
    let program = $('#code').val()

    $.ajax({
        // url:'http://60.205.211.19:3008/compile',
        // url:'http://localhost:3008/compile',
        url:`http://${host}:${port}/compile`,
        type:'post',
        headers:{
            'Content-Type':'application/json'
        },
        data:JSON.stringify({
            src:program
        }),
    
        success:function(res){
            resetResult()  //重制所有结果展示
            $('.download-outputs').removeAttr('disabled')
            lastProgramName = res.program_name

            /************************  词法分析  ***************************/
            let lexErrList = JSON.parse(res.lex_err)        //词法分析错误  
            if(lexErrList && lexErrList.length > 0){
                //词法错误，报错
                setLexErr(lexErrList)
                scrollToResult()    //结果展示
                return
            }
            let tokenList = JSON.parse(res.tokens)  //获得token序列
            resetTokenList(tokenList)             //追加token列表

            /************************  语法分析  ***************************/
            let synErrList = JSON.parse(res.syn_err)//递归下降错误
            let ll1ErrList = res.syn_ll1_err        //ll1错误
            
            console.log(synErrList)
            if(synErrList[0] != ''){
                //语法错误
                setSynErr(synErrList,ll1ErrList)
                scrollToResult()
                return
            }

            let rdtree     = res.tree                       //递归下降语法树
            let ll1tree    = res.treell1                    //ll1语法树
            resetSyntaxTree(rdtree,ll1tree)

            gene = res.gene
            comments = JSON.parse(res.comments)
            resetCode(gene,comments)
        }
    })
})

//下载编译产物
$('.download-outputs').on('click',function(){
    url = `http://${host}:${port}/zips/${lastProgramName}.zip`

    window.open(url)
})

//重置按钮
$('.btn-reset').on('click',function(){
    if(!confirm('是否清空当前内容？')){
        return
    }
    $('.download-outputs').attr('disabled','disabled')
    resetCode('',[])
    resetTokenList([])
    resetSyntaxTree('')
})

//选择模板
$('.demo-programs').on('change',function(){
    file = $('.demo-programs').val()
    $.ajax({
        // url:'http://localhost:3008/demoProgram',
        // url:'http://60.205.211.19:3008/demoProgram',
        url:`http://${host}:${port}/demoProgram`,
        type:'get',
        data:{
            file:file
        },
        success:function(res){
            // console.log(res)
            resetCode(res.demo,[])
            resetResult()
        }
    })
})

//展示语义结果
function resetSemList(sem){
    let semlist = []
    let semlen = 0
    let currSemBlock
    for(let i of sem){
        if(i.level_flag.length > 0){
            currSemBlock = {
                level : i.level_flag,
                list: []
            }
            semlist[semlen++] = currSemBlock
            continue
        }
        currSemBlock.list.push(i)
    }
    console.log(semlist)
    $('.sem-res-body').empty()
    for(block of semlist){
        for(let i = 0;i < block.list.length;i++){
            let semitem = block.list[i]
            let tr
            if(i == 0){
            tr = $(`<tr class="sem-item-level">
                        <td ${i==0?'rowspan="'+block.list.length+'"':''}>${block.level}</td>
                        <td>${semitem.name}</td>
                        <td>${semitem.kind}</td>
                        <td>${semitem.type_}</td>
                        <td>${semitem.noff}</td>
                        <td>${semitem.offset}</td>
                        <td>${semitem.dir}</td>
                    </tr>`)
            }else{
                tr = $(`<tr class="sem-item-non-level">
                        <td>${semitem.name}</td>
                        <td>${semitem.kind}</td>
                        <td>${semitem.type_}</td>
                        <td>${semitem.noff}</td>
                        <td>${semitem.offset}</td>
                        <td>${semitem.dir}</td>
                    </tr>`)
            }
            $('.sem-res-body').append(tr)
        }
    }
}

//展示语义错误
function setSemErr(semErrList){
    if(semErrList && semErrList.length != 0){
        //存在语义错误
        $('.sem-errs').addClass('errs')
        $('.sem-errs h3').text('Ops! semantic errros!')
        for(let err of semErrList){
            $('.sem-err-list').append(
                $(`<div class="sem-err">${err}</div>`)
            )
        }
        // alert('语义错误！')
        return
    }
}

//展示词法错误
function setLexErr(lexErr){
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
    }
}

//展示语法错误
function setSynErr(synErr,ll1Err){
    if(synErr && synErr != ''){
        $('.syn-errs').addClass('errs')
        $('.syn-errs h3').text('Ops! syntax errors!')
        $('.syn-err-list').html(`<li>${ll1Err}</li><li>${synErr}</li>`)
        flag = false
    }
}

function scrollToResult(){
    $('html, body').animate({scrollTop: $('.errors').offset().top}, 300) 
}

// function resetErrorPanel(lexErr,synErr,semErr){
//     //清除errs类
//     $('.lex-errs').removeClass('errs')
//     $('.syn-errs').removeClass('errs')
//     $('.sem-errs').removeClass('errs')
//     //清空展示列表
//     $('.lex-err-list').empty()
//     $('.syn-err-list').html('')
//     //重置文字
//     $('.lex-errs h3').text('Great!No lexical error!')
//     $('.syn-errs h3').text('Great!No Syntax error!')
//     $('.sem-errs h3').text('Great!No Sematic error!')

//     let flag = true
//     //词法分析错误
//     if(lexErr && lexErr.length > 0){
//         $('.lex-errs').addClass('errs')
//         $('.lex-errs h3').text('Ops! lexical errros!')
//         for(let err of lexErr){
//             $('.lex-err-list').append(
//                 $(`<div class="lex-error">
//                         <div class="lex-error-pos">${err.line},${err.col}</div>
//                         <div class="lex-error-detail">${err.err}</div>
//                     </div>`)
//             )
//         }
//         flag = false
//     }

//     //语法分析错误
//     if(synErr && synErr != ''){
//         $('.syn-errs').addClass('errs')
//         $('.syn-errs h3').text('Ops! syntax errors!')
//         $('.syn-err-list').html(synErr)
//         flag = false
//     }
//     return flag
// }

//重置结果区域
function resetResult(){
    /***********************  错误模块  ***************************/
    //清除errs类
    $('.lex-errs').removeClass('errs')
    $('.syn-errs').removeClass('errs')
    $('.sem-errs').removeClass('errs')
    //清空错误列表
    $('.lex-err-list').empty()
    $('.syn-err-list').html('')
    $('.sem-err-list').empty()
    //重置文字
    $('.lex-errs h3').text('Great!No lexical error!')
    $('.syn-errs h3').text('Great!No Syntax error!')
    $('.sem-errs h3').text('Great!No Sematic error!')

    /***********************  结果模块  ***************************/
    $('.tokenlist').empty()
    $('.linenos').empty()
    $('.tree').val('')
    $('.sem-res-body').empty()
}

function currRemSize(){
    let fontSize = $('html').css('font-size')
    fontSize = fontSize.substring(0,fontSize.length-2)
    return Number(fontSize)
}

function resetCode(program,comments){
    lines = program.split('\n')
    // console.log(lines)
    // console.log(comments)
    program = ''
    for(let i = 0;i < lines.length;i++){
        let line = i + 1
        for(let comment of comments){
            if(comment.line == line){
                lines[i] += ` {${comment.comment}}`
            }
        }
        program += lines[i] + '\n'
    }

    $('.code').val(program)
    resetLines()
}

function resetSyntaxTree(rdtree,ll1tree){
    // 递归下降处理
    let rdwd = 0
    let rdht = 0
    lines = rdtree.split('\n')
    for(line of lines){
        let tmp = 0
        for(ch of line){
            tmp += ch == '\t' ? 4 : 1
        }
        rdwd = Math.max(rdwd,tmp)
    }
    rdht = lines.length
    $('.syntax-tree-rd .tree').width(currRemSize() * 1 * rdwd)
    $('.syntax-tree-rd .tree').height(currRemSize() * 1.125 * rdht + 5)
    $('.syntax-tree-rd .linenos').height(currRemSize() * 1.125 * rdht + 5)
    $('.syntax-tree-rd .tree').val(rdtree)
    $('.syntax-tree-rd .linenos').empty()
    for(let i = 1;i <= rdht;i++){
        $('.syntax-tree-rd .linenos').append(
            `<div class="lineno">${i}</div>`
        )
    }
    //  ll1处理
    let ll1wd = 0
    let ll1ht = 0
    lines = rdtree.split('\n')
    for(line of lines){
        let tmp = 0
        for(ch of line){
            tmp += ch == '\t' ? 4 : 1
        }
        ll1wd = Math.max(ll1wd,tmp)
    }
    ll1ht = lines.length
    $('.syntax-tree-ll1 .tree').width(currRemSize() * 0.8 * ll1wd)
    $('.syntax-tree-ll1 .tree').height(currRemSize() * 1.125 * ll1ht + 5)   
    $('.syntax-tree-ll1 .linenos').height(currRemSize() * 1.125 * rdht + 5) 
    $('.syntax-tree-ll1 .tree').val(ll1tree)
    $('.syntax-tree-ll1 .linenos').empty()
    for(let i = 1;i <= rdht;i++){
        $('.syntax-tree-ll1 .linenos').append(
            `<div class="lineno">${i}</div>`
        )
    }
    
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
    $('.code').css({height:`${lines*1.5+0.25}rem`})
}

function resetDemoList(){
    $('.demo-programs').empty()
    $.ajax({
        // url:'http://localhost:3008/demoProgramList',
        // url:'http://60.205.211.19:3008/demoProgramList',
        url:`http://${host}:${port}/demoProgramList`,
        type:'get',
        success:(res)=>{
            // console.log(res)
            for(let program of res){
                $('.demo-programs').append(
                    $(`<option value="${program}">${program}</option>`)
                )
            }
            if(res.length >= 1){
                $('.demo-programs').change()
            }
        }
    })
}

resetLines(20)
resetDemoList()