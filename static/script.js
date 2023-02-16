function initMap() {
    $('.building').click(function() {
      var companyId = $(this).data('company-id');
      $.ajax({
        url: '/company-details/' + companyId,
        method: 'GET',
        success: function(data) {
          var content = '<h2>' + data.name + '</h2>';
          content += '<p>' + data.description + '</p>';
          content += '<p>Funding goal: $' + data.funding_goal + '</p>';
          content += '<p>Funding raised: $' + data.funding_raised + '</p>';
          content += '<div class="investments">';
          content += '<h3>Investors</h3>';
          content += '<table>';
          content += '<thead><tr><th>Name</th><th>Invested Amount</th></tr></thead>';
          content += '<tbody>';
          for (var i = 0; i < data.investors.length; i++) {
            content += '<tr><td>' + data.investors[i].name + '</td><td>$' + data.investors[i].invested_amount + '</td></tr>';
          }
          content += '</tbody>';
          content += '</table>';
          content += '</div>';
          $('.company-details .content').html(content);
          $('.company-details').show();
        },
        error: function() {
          alert('Error fetching company details');
        }
      });
    });
  
    $('.close-details').click(function() {
      $('.company-details').hide();
    });
  }
  