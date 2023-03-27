<template>
    <div class="text-center">
        
          <h1 class="text-success fs-1 m-4">Welcome to your profile, {{ user.username}}. </h1>
  
          <div class="d-flex justify-content-center">
            <div class="d-flex flex-column mx-2">
              <div class="d-flex flex-column mx-4 flex-fill">
                <img loading="auto" class="user-img rounded-top" :src="user.profile_image" :alt="user.profile_image"  width="200" height="200"/>
                <button class="btn btn-secondary m-0 rounded-0 rounded-bottom flex-fill"
                type = "button" data-bs-toggle="collapse"  data-bs-target="#editimageCard"
                aria-expanded="false" aria-controls="editimageCard">Change profile picture</button> 
              </div>
          </div>
          <div class="align-self-center">
            <table class="table text-start m-2 p-2" >
            <tr>
                <td class = "col-md-5">Email:</td>
                <td class = "col-md-5">{{ user.email }}</td>
            </tr>
            <tr>
                <td class = "col-md-5">Date of Birth: </td>
                <td class = "col-md-5">{{ user.date_of_birth }}</td>
            </tr>
            <tr>
                <td class = "col-md-5">City:</td>
                <td class = "col-md-5">{{ user.city }}</td>
            </tr>
            </table>
            <button class="btn btn-secondary m-3 "
          type = "button" role="button" data-bs-toggle="collapse"  data-bs-target="#editListingCard"
          aria-expanded="false" aria-controls="editListingCard">Edit Profile</button> 
          </div>
  
          </div>
  
          <div class="collapse" id="editimageCard">
            <div class="card card-body shadow text-center mx-5">
                <form @submit="uploadImage" enctype="multipart/form-data">
                  <h3>Update Profile Image</h3>
                      <input class="d-block form-control" type="file" accept="image/*" name="image" id="image"/>
                      <button class="btn btn-outline-secondary m-3"
                      type = "button" data-bs-toggle="collapse"  data-bs-target="#editimageCard"
                      aria-expanded="true" aria-controls="editimageCard">Cancel</button>
                    <button class="btn btn-success m-3" type="submit">Change Image</button>
                </form>
              </div>
            </div>
          
          
          <div class="collapse" id="editListingCard">
          <div class="card-body shadow text-center mx-5">
                  <div class="card card-body px-5 ">
                      <h3>Edit Information</h3>
                      <div class="input-group mb-3">
                          <span class="input-group-text">Username</span>
                        <input type="text" class="form-control" :id="'usernameid' + user.id"
                      ref="username_ref_" :value="user.username" required/>
                      </div>
                      <div class="input-group mb-3">
                          <span class="input-group-text">Email</span>
                          <input type="text" class="form-control" :id="'emailid' + user.id" 
                        ref="email_ref" :value="user.email" required/>
                      </div>
                      <div class="row">
                        <div class="col-6">
                          <div class="input-group mb-3">
                              <span class="input-group-text">Date of birth</span>
                              <input type="date" class="form-control" :id="'date_of_birthid' + user.id" 
                              ref="date_of_birth_ref" :value="user.date_of_birth" required/>
                          </div>
                        </div>
                        <div class="col-6">
                          <div class="input-group mb-3">
                              <span class="input-group-text">City</span>
                              <input type="text" class="form-control" :id="'cityid' + user.id" 
                          ref="city_ref" :value="user.city" required/>
                          </div>
                          
                        </div>
                    </div>
                    <div>
                      <button class="btn btn-outline-secondary m-3"
                        type = "button" role="button" data-bs-toggle="collapse"  data-bs-target="#editListingCard"
                        aria-expanded="true" aria-controls="editListingCard">Cancel</button> 
                      <button class="btn btn-success" @click="putData(user.id)">Save changes</button>
                    </div>
                      
  
                  </div>
              </div>
          </div>
        
  
          
    </div>
  
  </template>
  
  <script lang="ts">
  import { defineComponent, useSSRContext } from 'vue'
   export default defineComponent( {
    name: 'App',
    data: () => {
      return{
        user: [] as any,
        users: [] as {id: number, date_of_birth: string, city: string, username: string, email: string}[],
      };
    },
    mounted(){
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
        } ,
        
        
      getUserDetails(id : number,) {
        let user : {username: string, email: string, date_of_birth: string, city: string} [] = [ 
     
            {
              "username": (<HTMLInputElement> document.querySelector(`#usernameid${id}`)).value,
              "email": (<HTMLInputElement>document.querySelector(`#emailid${id}`)).value,
              "date_of_birth":(<HTMLInputElement>document.querySelector(`#date_of_birthid${id}`)).value,
              "city":(<HTMLInputElement> document.querySelector(`#cityid${id}`)).value 
            }
      
        ];
        return user
      },
      uploadImage(event: any) {
        // Prevent the default form submission
        event.preventDefault();
        // Get the form data
        let formData = new FormData()
        var input: any = document.getElementById('image');
        var profile_image  = input.files[0];
        formData.append('profile_image', profile_image)
        if (!profile_image) {
                      alert("You have to choose an image file first!");
                      return;
                  }
        // Make a POST request to the Django server with the form data
        fetch('/api/user/', {
          method: 'POST',
          credentials: "include",
          mode: "cors",
          referrerPolicy: "no-referrer",
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.fetchUser()
        })
        .catch(error => {
          console.error(error);
        });
      },
      async putData(user_id : number) {
          let user = this.getUserDetails(user_id)
          console.log(user)
          console.log(user [0])
          let response = await fetch("/api/user/",{
            
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    method: "PUT",
                    headers: { "Content-Type": "application/json",
                              "Accept": "application/json"
                   },
                    body: JSON.stringify(user[0]),
            });
          if(response.ok){
            this.fetchUser();
            alert(`Your profile was successfully edited`);
          }
          else{
            alert("Fill in all fields");
          }
        },
    
      }
      })
  </script>