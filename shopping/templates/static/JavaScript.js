$(document).ready(function() {
    $('.add-to-cart-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(data) {
                if (data.success) {
                    $('#cart-btn').text('Cart (' + data.cartTotalQuantity + ')');
                }
            },
            error: function(xhr, status, error) {
                if (xhr.status === 403) {
                    alert(xhr.responseJSON.error);
                    window.location.href = '/login/?next=' + window.location.pathname;
                } else {
                    console.log('An error occurred: ' + error);
                }
            }
        });
    });

    function clearCart() {
        $.ajax({
            url: "{% url 'clear_cart' %}",
            type: "POST",
            data: {},
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(data) {
                if (data.success) {
                    $('#cart-btn').text('Cart (0)');
                    console.log('Cart has been cleared.');
                }
            },
            error: function() {
                console.log('An error occurred while clearing the cart.');
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});



{% comment %} // 引入 Plotly.js
document.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"><\/script>');

// Bar Chart 1: Creator Counts
var creatorData = [{
    x: creator_ids,
    y: creator_counts_list,
    type: 'bar'
}];
var creatorLayout = {
    title: '创建者ID vs 数量',
    xaxis: { title: '创建者ID' },
    yaxis: { title: '数量' }
};
Plotly.newPlot('creator_counts_chart', creatorData, creatorLayout);

// Bar Chart 2: Last Modified Counts
var lastModifiedData = [{
    x: last_modified_ids,
    y: last_modified_counts_list,
    type: 'bar'
}];
var lastModifiedLayout = {
    title: 'Last Modified By ID vs Count',
    xaxis: { title: 'Last Modified By ID' },
    yaxis: { title: 'Count' }
};
Plotly.newPlot('last_modified_counts_chart', lastModifiedData, lastModifiedLayout);

// 点击事件监听
var lastModifiedChart = document.getElementById('last_modified_counts_chart');
lastModifiedChart.on('plotly_click', function(data){
    var lastModifiedId = data.points[0].x;  // 获取点击的 Last Modified ID
    window.location.href = '/last_modified_by_creator/' + lastModifiedId + '/';  // 重定向到 Last Modified By Creator 页面
}); {% endcomment %}
