var apigClient = apigClientFactory.newClient();


function search_photos() {
  console.log("search_photos");
  var search_term = $('#transcript').val();
  console.log(search_term);

  var params = {
    'q': search_term
  };

  var additionalParams = {
    headers: {
      'x-api-key': 'QtTlr0aoKn382w1ElTaJg6znh8JfK19x4CCEkJOt'
    }
  }

  apigClient.searchGet(params, {}, additionalParams).then(
    function (result) {
      image_urls = result["data"];
      console.log(image_urls);

      image_inner_html = $('#images');
      image_inner_html.html('');

      for (var i = 0; i < image_urls.length; i++) {
        image_inner_html.append('<img src="' + image_urls[i] + '></img>');
        console.log('<img src="' + image_urls[i] + '></img>');
      }

    }
  ).catch(function (result) {
    console.log(result);
  });

}


function upload_photos() {
  console.log("upload_photos");

  var file_path = $('#file').val().split('\\');
  var file_name = file_path[file_path.length - 1];

  var file = $('#file')[0].files[0];

  var additional_labels = $('#labels').val();
  console.log(additional_labels);

  var additional_params = {
    headers: {
      'Content-Type': file.type,
      'x-api-key': 'QtTlr0aoKn382w1ElTaJg6znh8JfK19x4CCEkJOt',
      'x-amz-meta-customLabels': additional_labels
    }
  }

  var url = 'https://s3.amazonaws.com/cs-gy-9223-b2/' + file_name;

  axios.put(url, file, additional_params).then(
    function (result) {
      console.log(result);
    }
  ).catch(function (result) {
    console.log(result);
  });
}