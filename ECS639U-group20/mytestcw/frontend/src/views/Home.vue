<template>
    <div class="d-flex justify-content-around m-2">
        <div class="mr-4 p-0 input-group">
            <input type="text" class="form-control rounded-0 rounded-start" placeholder="Find an item..." id = "searchId">
            <button class="btn btn-success rounded-0 rounded-end" type="button" id="search-btn" @click="filter()">Search</button>
        </div>
        <div class="mx-1 p-0">
            <router-link :to="{ name: 'Posting' }" custom v-slot="{ navigate }">
                <button class="mx-2 btn btn-outline-primary" type="button" id="add-btn" @click="navigate" role="link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                    </svg>
                </button>
            </router-link>
        </div>
    </div>
    <div class="d-flex justify-content-center m-2">
        <div class="mx-1 p-0">
            <button v-if="filtered" class="btn btn-outline-danger" type="button" id="search-btn" @click="removeFilter()">Remove Search Filter</button>
            <button v-else class="btn btn-outline-secondary" type="button" id="search-btn" disabled>Remove Search Filter</button>
        </div>
        <div class="mx-1 p-0">
            <button v-if="!available" class="btn btn-outline-secondary mx-1" type="button" @click="availableProducts()">Show Available</button>
            <button v-else class="btn btn-outline-secondary mx-1" type="button" @click="allProducts()">Show All</button>
        </div>
    </div>

        
        

    <!-- LIST of ITEMS in card -->
    <div class="row my-5">
         <div v-for="eachItem in items" class="col-sm-6 col-md-4 col-lg3 p-0">
             <router-link :to="{ name: 'Item', params : {id: eachItem.id}}" custom v-slot="{ navigate }" >
                 <div class="card p-0 m-1 eachItemCard" style="height: 20rem;" @click="navigate">
                     <img loading="auto" :src="eachItem.picture" class="card-img-top" height="180">
                     <div class="card-body py-1 px-3">
                         <h4 class="card-title d-flex justify-content-start m-0 text-nowrap overflow-auto">{{ eachItem.title }}</h4>
                         <p class="card-text text-muted"><small class="font-weight-bold float-start">Starting from £{{ eachItem.starting_price }}</small></p> <br>
                         <p class="card-text d-flex justify-content-start m-0 text-muted">Bid ends:</p>
                         <p class="card-text d-flex justify-content-start m-0 text-primary fw-bold">{{ formatDate(eachItem.deadline) }}</p>

                     </div>
                 </div>
     </router-link>
         </div>
     </div>
</template>


<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    data(){
        return{
            item: [] as any,
            items: [] as {id: number, title: string, description: string, deadline: string, starting_price: string, picture: string, user: string}[],
            filtered: false,
            available: false,
        };
    },
    props: {
        user_id: Number,
    },
    mounted(){
        this.fetchItems()
    },
    methods:{
        async fetchItems(){
            let response = await fetch("/api/items/",{
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
            });
            let data = await response.json()
            console.log(data)
            this.items = data.items 
            // for(const item of this.items){
            //     item.picture = "http://localhost:8000" + item.picture
            // }
        } ,
        async fetchItem(item_id: number){
            let response = await fetch("/api/item/" + item_id);
            let data = await response.json()
            this.item = data
            // this.item.picture = "http://localhost:8000" + this.item.picture
            console.log(data)
            console.log(this.item)
        } ,
        formatDate(deadline: string) {
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var date = new Date(deadline)
        let day = date.getDate()
        let month = monthNames[date.getMonth()]
        let year = date.getFullYear()
        var strDate = day + " " + month + " " + year
        var hours = date.getHours();
        var minutes:number|string = date.getMinutes();
        var ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        minutes = minutes < 10 ? '0' + minutes : minutes;
        var strTime = hours + ':' + minutes + ' ' + ampm;
        return (strDate + "  " + strTime);
        },
        async filter(){
            let response = await fetch("/api/items/",{
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
            });
            let data = await response.json()
            console.log(data)
            this.items = data.items
            var filteredResults = []
            let value = (<HTMLInputElement>document.getElementById("searchId")).value;
            value = value.toLowerCase()
            console.log(value)
            let x = value.replace(/[^A-Za-z0-9]+/g, " ");
            let newArr = x.trim().split(" ");
            console.log(newArr);
            for (let i = 0; i < this.items.length; i++){
                var check = false
                for (let j = 0; j < newArr.length && check === false; j++){
                    var item_title=this.items[i].title.toLowerCase()
                    var item_description=this.items[i].description.toLowerCase()
                    if(item_title.includes(newArr[j]) || item_description.includes(newArr[j]))check=true
                }
                if (check) filteredResults.push(this.items[i])
            }
            console.log(filteredResults)
            this.items = filteredResults
            this.filtered = true;
        },
        async removeFilter(){
            this.fetchItems()
            this.filtered = false;
            (<HTMLInputElement>document.getElementById("searchId")).value = ""
        },
        async availableProducts(){
            let response = await fetch("/api/items/",{
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
            });
            let data = await response.json()
            console.log(data)
            this.items = data.items 
            this.items = this.items.filter((x) => { return new Date(x.deadline)>new Date();});
            this.available = true;
        } ,
        async allProducts(){
            let response = await fetch("/api/items/",{
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
            });
            let data = await response.json()
            console.log(data)
            this.items = data.items 
            this.available = false;
        } ,
    },
    
});
</script>

<style>
img{
    object-fit: cover;
}
.eachItemCard{
    transition: 0.2s;
}
.eachItemCard:hover {
    cursor: pointer;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}
#search{
    margin: 0;
}
</style> 