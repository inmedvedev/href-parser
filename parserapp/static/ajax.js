$(document).ready(() => {
  console.log('Sanity Check!');
});

let frm = $('#parseSubmit');
frm.submit( function() {

  jQuery.ajax({
    type: frm.attr('method'),
    url: '',
    data: frm.serialize(),
  })
  .done((data) => {
    let search_url =  "?url=" + encodeURIComponent(data.url) + "&task=" + data.task_id;
    getData(search_url);
    console.log(data);
  })
  .fail((err) => {
    console.log(err);
  });
  return false;
});


function getData(url) {
  jQuery.ajax({
  url: url,
  type: "GET",
  dataType: "json",
  success: (data) => {
    let html = ``
    $.each(data.data, function(k, v){
      html+= `
      <tr>
        <td>${v.id}</td>
        <td>${v.url}</td>
        <td>${v.domain}</td>
        <td>${v.create_date}</td>
        <td>${v.update_date}</td>
        <td>${v.country}</td>
        <td>${v.is_dead}
      </tr>`
    });
    $('#data').empty();
    $('#data').html(html);
    const taskStatus = data.task_status.task_status;
    $('#taskStatus').empty();
    $('#taskStatus').html(taskStatus)
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    console.log(data);
    setTimeout(function() {
      getData(url);
    }, 3000);
  },
  error: (error) => {
    console.log(error);
  }
})
}
