<template>
    <!-- upload item-->
    <div class="bg-light mt-4 mx-5 py-4 rounded shadow text-center">
        <h2 class="text-success mx-4 pb-2">Upload an item for bidding</h2>
        <form @submit="addItem" enctype="multipart/form-data" class="mx-5 px-5">
            <input class="form-control my-2" id="title2" type="text" placeholder="Title" required>
            <textarea class="form-control my-2" id="description2" type="text" placeholder="Description" rows="4" required></textarea>
            <div class="row">
                <div class="col-6">
                    <input class="form-control" id="deadline2" type="datetime-local" placeholder="Deadline" required>
                </div>
                <div class="col-6">
                    <input class="form-control" id="starting_price2" type="number" min="1" placeholder="Starting Price (£)" step="0.50" required>
                </div>
            </div>
            <input class="form-control mt-2" type="file" accept="image/*" id="picture2" required>
            <small class=" mb-2 d-flex justify-content-start text-muted fst-italic"> *Upload a picture of your item</small>
            <router-link :to="{ name: 'Home' }" custom v-slot="{ navigate }">
                <button @click="navigate" role="link" class="btn btn-outline-secondary m-2"> Cancel</button> 
            </router-link>
            <button type="submit" class="btn btn-primary m-2"> Post item</button>

        </form>
    </div>
</template>


<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    methods:{
        async addItem(event:any){
            event.preventDefault();
            let itemFormData = new FormData();
            var input: any = document.getElementById('picture2');
            var new_picture = input.files[0];
            console.log(new_picture)
            let new_title = (<HTMLInputElement>document.getElementById("title2")).value;
            let new_description = (<HTMLInputElement>document.getElementById("description2")).value;
            let new_deadline = (<HTMLInputElement>document.getElementById("deadline2")).value;
            let new_starting_price = (<HTMLInputElement>document.getElementById("starting_price2")).value;
            let new_entry = {
                title: new_title,
                description: new_description,
                deadline: new_deadline,
                staring_price: new_starting_price,
            }
            console.log(new_entry)
            itemFormData.append('title', new_title);
            itemFormData.append('description', new_description);
            itemFormData.append('deadline', new_deadline);
            itemFormData.append('starting_price', new_starting_price);
            itemFormData.append('picture', new_picture);
            // formData.append('user', JSON.stringify(current_user))
            console.log("this is form data")
            console.log(itemFormData)
            let response = await fetch("/api/items/",{
                method: 'POST',
                mode: 'cors',
                credentials: 'include',
                referrerPolicy: "no-referrer",
                body: itemFormData,
            });
            if(response.ok){
                (<HTMLInputElement>document.getElementById("title2")).value = "",
                (<HTMLInputElement>document.getElementById("description2")).value = "",
                (<HTMLInputElement>document.getElementById("deadline2")).value = "",
                (<HTMLInputElement>document.getElementById("starting_price2")).value = "",
                (<HTMLInputElement>document.getElementById("picture2")).value = ""
                this.$router.push('/');
            }
            else
                alert("Item cannot be added. Try again later");
        },
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
    },
    
});
</script>

<style>
img{
    object-fit: cover;
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
    width: 80%;
    margin:4% 10%;
}
</style> 