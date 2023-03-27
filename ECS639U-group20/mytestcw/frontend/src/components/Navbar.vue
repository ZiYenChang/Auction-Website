<template>
    <nav class="navbar navbar-expand-lg bg-light">
        <div class="container-fluid">
            <div>
                <router-link :to="{ name: 'Home' }" custom v-slot="{ navigate }">
                    <button @click="navigate" role="link">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-house"
                            viewBox="0 0 16 16">
                            <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.707 1.5ZM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5 5 5Z" />
                        </svg>
                    </button>
                </router-link>
                <router-link to="/userprofile" custom v-slot="{ navigate }">
                    <button v-if="user.username" @click="navigate" role="link">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor"
                                class="bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                                <path fill-rule="evenodd"
                                    d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z" />
                        </svg>
                    </button>
                </router-link>
            </div>
            <span class="navbar-text">
                <a v-if="!user.username" href="/accounts/login/">Sign In/Register</a>
                <svg v-if="!user.username" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor"
                            class="bi bi-person-circle" viewBox="0 0 16 16">
                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                            <path fill-rule="evenodd"
                            d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z" />
                </svg>   
                
                    <div v-if="user.username">
                        <button @click="logout()" role="link">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-box-arrow-right"
                            viewBox="0 0 16 16">
                            <path fill-rule="evenodd"
                                d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z" />
                            <path fill-rule="evenodd"
                                d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z" />
                        </svg>
                        </button>
                    </div>
                
            </span>
        </div>
    </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import QandA from './QandA.vue';
import Bid from './Bid.vue';

export default defineComponent({
    data(){
      return{
        items: [] as {id: number, title: string, description: string, deadline: string, starting_price: number, user: string}[],
        item: [] as any,
        user: [] as any,
      };
    },
    components:{
        QandA,
        Bid,
    },
    mounted() {
        this.fetchUser()
    },
    methods: {
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
      },
      logout(){
             window.location.href = "/accounts/logout/"
      }
    }
})
</script>

<style scoped>
a {
  text-decoration: none; /* no underline */
  padding-right: 1em;
}
</style>