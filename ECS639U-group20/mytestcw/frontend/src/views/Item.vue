<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-4">
                <img loading="auto" :src="item.picture" class="rounded float-left" alt="..." width="300">
            </div>
            <div class="col-sm-8">
                <h1>{{item.title}}</h1>
                <div v-if="item.user === user.id">
                  <small class="text-primary fw-bold"> {{user.username}}, you are the seller of this item.</small>
                </div>
                <hr/>
                <small class="text-muted">{{item.description}}</small>
                <Bid :item_id="id" :user_id="user.id" />
                <div class="qa">
                    <h3>Customer questions & answers</h3>
                    <QandA :user_id="user.id" :item_id="id"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import QandA from '/src/components/QandA.vue';
import Bid from '/src/components/Bid.vue';
import Navbar from '/src/components/Navbar.vue';


export default defineComponent({
    data(){
      return{
        item: [] as any,
        user: [] as any,
        // id: this.$route.params.id
      };
    },
    components:{
        QandA,
        Bid,
        Navbar,
    },
    props: ['id'],
    mounted() {
      this.getItem(this.id)
      this.fetchUser()
    },
    methods: {
      async getItem(item_id: number){
        let response = await fetch("/api/item/" + item_id);
        let data = await response.json();
        this.item = data;
      },
      async fetchUser(){
        // perform an Ajax request to fetch the list of users
        let response = await fetch("/api/user/",{
                  credentials: "include",
                  mode: "cors",
                  referrerPolicy: "no-referrer",
        });
        let data = await response.json()
        console.log(data)
        this.user = data.user
      } ,
    }
})
</script>

<style scoped>
img {
    margin: 10% 0 0 0;
}
h1{
    margin: 3% 0 0 0;
}
.qa{
    margin-top: 8%;
    margin-left: 2%;
}
</style>