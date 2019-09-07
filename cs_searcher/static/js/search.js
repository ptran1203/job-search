
template_map = {
    1: `
    <div class="search-result">
  <div class="icon">
    <img src="#post_img#" width="200" />
  </div>
  <div class="content">
    <h4 id="jobtitle" onclick="viewDetail(#docid#)">#title#</h4>
    <a href="#post_url#">Goto page</a>
    <p>
      <span class="salary">#salary_range#</span>
    </p>
    <div>
      <p>#content#</p>
      <p class="more-content">#more_content#</p>
    </div>
    <div class="actions">
      <span class="date">#post_date#</span>
      <span class="save"><a href="/save">save job</a></span>
      <span class="email"><a href="/email">email</a></span>
    </div>
  </div>
</div>
    `,
  2: `
  <div>#word#<div>
  `
}


function generate_html(item, templateId) {
  let content = template_map[templateId] || '',
    data = item.fields

  data.docid = item.pk
  // data['more_content'] = data.content.slice(0, 200) + '....'
  Object.keys(data).map(record => {
    let key = '#' + record + '#'
    content = content.split(key).join(data[record])
  })

  return content
}

function viewDetail(pk) {
  let instance = document.getElementById('detail')
  console.log(instance);
  const xhr = new XMLHttpRequest()
  xhr.open('GET', '/api/post/' + pk)
  xhr.onload = function () {
    if (xhr.status == 200) {
      console.log(xhr.response);
    }
  }
  xhr.send()
}

/**
 * Jquery
 */
jQuery(document).ready(function() {
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
  $('#search-form').on('submit', function(e) {
    e.preventDefault()
    let inputBox = $('.js-searchBox-input'),
      instance = $("#jobs"),
      query = inputBox.val()
    
    $.ajax({
      url : '/api/search?q=' + query,
      method : "GET",
      beforeSend: function() {
        instance.html('')
        instance.addClass("spinner")
      },
      success : function(data){
        instance.removeClass("spinner")
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