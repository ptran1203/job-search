
template_map = {
    1: `
    <div class="search-result">
  <div class="icon">
    <img src="#post_img#" width="60" />
  </div>
  <div class="content">
    <h2><a href="#post_url#">#title#</a></h2>
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
    `
}

function generate_html(data, templateId) {
  let content = template_map[templateId] || ''

  data.content = data.content.slice(0, 70) + '....'
  Object.keys(data).map(record => {
    let key = '#' + record + '#'
    content = content.split(key).join(data[record])
  })

  return content
}

/**
 * Jquery
 */
jQuery(document).ready(function() {
  $('.js-clearSearchBox').css('opacity', '0')
  $('.js-searchBox-input').keyup(function() {
    if ($(this).val() !='' ) {
      $('.js-clearSearchBox').css('opacity', '1')
    } else {
      $('.js-clearSearchBox').css('opacity', '0')
    }
  })
  // click the button 
  $('.js-clearSearchBox').click(function() {
    $('.js-searchBox-input').focus()
    $('.js-clearSearchBox').css('opacity', '0')
  })

  function formatData(item) {
    return `
    <div>
      <strong style="display: block">
      <a href="${item.post_url}" target="blank">${item.title}</a>
      </strong>
      <p>${item.content.slice(0, 50)}</p>
    </div>
    `
  }
  // Ajax get search data
  $('#search-form').on('submit', function(e) {
    e.preventDefault()
    let inputBox = $('.js-searchBox-input'),
      instance = $(".jobs"),
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
          acc += generate_html(item.fields, 1)
          return acc
        }, '')

        instance.append(html)
        // Set default
        inputBox.val('')
      },
      error: function(error){
        console.log(error)
      }
    })
  })
})