// event handler for button for class update-cart
// learn from https://www.youtube.com/watch?v=woORrr3QNh8&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=4
var updateBtns = document.getElementsByClassName('update-cart')

for(let value of updateBtns){
    value.addEventListener('click', function(){ // add type click
        var bookIsbn = this.dataset.product //product here is from data-product
        var action = this.dataset.action // add rent remove
        console.log('bookIsbn:', bookIsbn, 'action:', action) // will return bookIsbn and action in console browser
        console.log('USER:', user)

        // check if user log in or not
        if(user === 'AnonymousUser'){
            console.log('Not logged in') // console this if user isnt log in
        }else{
            updateUserOrder(bookIsbn, action) // if logged in then move to next function
        }
    })
}


function updateUserOrder(bookIsbn, action){
    console.log('User is logged in, sending data..')

    var url = '/update_item' // this is where we gonna sent the data to

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,    
        },
        body:JSON.stringify({'bookIsbn': bookIsbn, 'action':action}) // sent as string by using stringify
    })
    
    // return response
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
