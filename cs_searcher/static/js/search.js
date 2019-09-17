
const template_map = {
    1: `d
    <div class="search-result" pk="#id#" onclick="viewDetail(this)">
  <div class="icon">
    <img src="#post_img#" width="200" />
  </div>
  <div class="content">
    <h4 id="jobtitle">#title#</h4>
    <a href="#post_url#">Goto page</a>
    <p>
      <span class="salary">#salary_range#</span>
    </p>
    <div>
      <p>#content#</p>
    </div>
    <div class="actions">
      <span class="date">#post_date#</span>
      <span class="save"><a href="/save">save job</a></span>
      <span class="email"><a href="/email">email</a></span>
    </div>
  </div>
</div>
    `,
  3: `
  <div class="modal-dialog">
    <div class="modal-header">
    <h4><a href="#post_url#">#title#</a></h4>
    <a 
      href="#"
      class="btn-close closemodale"
      aria-hidden="true">
      &times;
    </a>
    </div>
    <div class="modal-body">
        <img src="#post_img#" width="200" style="display:block"/>
        <div class="far fa-money-bill-alt">  <span style="color:#fd8925">#salary_range#</span></div>
        <div class="job-desc" style="white-space: pre-line">#content#</div>
    </div>
    <div class="modal-footer">
        <a href="#post_url#" class="btn" id="btn_ingresar">Appy</a>
    </div>
  </div>
  `
}

let keywords = []

function generate_html(data, templateId) {
  let content = template_map[templateId] || ''
  Object.keys(data).map(record => {
    let key = '#' + record + '#'
    content = content.split(key).join(data[record])
  })

  return content
}

function activeElement(self) {
  let classList = self.className.split(' '),
    activeEle = document.getElementsByClassName('active')

  activeEle = activeEle[0]
  if (activeEle) {
    activeEle.classList.remove("active")
  }
  // remove all pre-active element

  if (!classList.includes('active')) {
    self.className += ' active'
  }
}

function viewDetail(self) {
  let ele = document.getElementById('detail')
  // beforsend
  ele.className += ' bar'
  ele.classList.remove('detail')

  const xhr = new XMLHttpRequest()
  const pk = self.getAttribute('pk')

  xhr.open('GET', '/api/post/' + pk)
  xhr.onload = function () {
    if (xhr.status == 200) {
      ele.className += ' detail'
      ele.innerHTML = generate_html(JSON.parse(xhr.response), 3)
      ele.style.overflowY = 'scroll'
      ele.classList.remove('bar')
      if (!ele.className.split(' ').includes('opened')) {
        ele.className += ' opened'
      }
      activeElement(self)
    }
  }
  xhr.send()
}

/**
 * Jquery
 */
jQuery(document).ready(function() {
  // get keywords in DB
  $.ajax({
    url : '/api/keywords',
    method : "GET",
    success : function(data){
      keywords = data
    },
    error: function(error){
      console.log(error)
    }
  })

  $.ajax({
    url : '/api/count',
    method : "GET",
    success : function(data){
      keywords = data
      $('input:text').attr('placeholder',`search for ${data.count || 0} jobs`);
    },
    error: function(error){
      console.log(error)
    }
  })


  // TODO: fix later
  // $('input[name=search]').on('input', function() {
  //   let ulTag = $('#autocomplete')
  //     ulTag.html('')

  //   let self = $('input[name=search]'),
  //     words = keywords.map(item => item.word),
  //     matches = words.filter(word => word.includes(self.val()))

  //   if (self.val()) {
  //     matches.forEach(function(word) {
  //       ulTag.append(`<li>${word}</li>`)
  //     })
  //   } else {
  //     ulTag.html('')
  //   }
  // })

  // Event handler
  $('.js-clearSearchBox').css('opacity', '0')
  $('.js-searchBox-input').keyup(function() {
    if ($(this).val() !='' ) {
      $('.js-clearSearchBox').css('opacity', '1')
    } else {
      $('.js-clearSearchBox').css('opacity', '0')
    }
  })
  $('.js-clearSearchBox').click(function() {
    $('.js-searchBox-input').focus()
    $('.js-clearSearchBox').css('opacity', '0')
  })

  // Ajax get search data
  $('#search-forms').on('submit', function(e) {
    e.preventDefault()
    let inputBox = $('.js-searchBox-input'),
      instance = $('#jobs'),
      query = inputBox.val()
    
    $.ajax({
      url : '/api/search?q=' + query,
      method : "GET",
      beforeSend: function() {
        instance.html('')
        instance.addClass("bar")
      },
      success : function(data){
        instance.removeClass("bar")
        let html = data.reduce((acc, item) => {
          // console.log(item.fields.pk);
          acc += generate_html(item, 1)
          return acc
        }, '')

        instance.append(html)
        
        $('#keywords').html(data.length + ' results: ' + query)
        // Set default
        inputBox.val('')
      },
      error: function(error){
        console.log(error)
      }
    })
  })
})