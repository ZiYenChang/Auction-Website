<template>
    <div class="card">
        <div class="card-body">
            <div class="row">
                <div class="col">
                    <p style="margin-left: 0.7rem;"><strong>Starting Price:</strong></p>
                    <p style="margin-left: 0.7rem;">£{{item.starting_price}}</p>
                </div>
                <div class="col">
                    <p><strong>Closes at:</strong></p>
                    <p>{{formatDate(item.deadline)}}</p>
                </div>
                <div v-if="bids.length!=0" class="col">
                    <p><strong> Last Bid:</strong></p>
                    <p>£{{max_bid}}<small class="text-muted"> [{{bids.length}} bids]</small></p>
                </div>
                <div v-else class="float-right col">
                    <p class="float-right"> </p>
                </div>
            </div>
            <div class="form-group row">
                <label v-if="bids.length!=0" for="inputBid" class="col-sm-4 col-form-label">Bid £{{max_bid+0.5}} or more:</label>
                <label v-else for="inputBid" class="col-sm-4 col-form-label">Bid £{{max_bid}} or more:</label>
                <div class="col-sm-8">
                    <input type="number" class="form-control" id="inputBid" placeholder="Bid Amount">
                </div>
            </div>
            <div class="row">
                
                <button style="margin: 0.7rem 0 0.3rem 0.7rem" v-if="new Date(item.deadline)>new Date()" @click="addBid()" type="button" class="btn btn-primary btn-block" id="inputBid">Place Bid</button>
                <button style="margin: 0.7rem 0 0.3rem 0.7rem" v-else type="button" class="btn btn-danger btn-block" id="inputBid" disabled>Bid Closed</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
    
    data(){
      return{
        bids: [] as {id: number, bid_amount: number, bid_time: string, item: string, user: string}[],
        top_bid: [] as any,
        item: [] as any,
        winner_id: 1,
        max_bid: 1,
      };
    },
    mounted() {
      this.getItem()
      this.getBids()
    },
    props: {
        item_id: Number,
        user_id: Number,
    },
    methods: {
        formatDate(deadline:string) {
            const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
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
      async getBids(){
        let response = await fetch("/api/bids/");
        let data = await response.json();
        this.bids = data.bids;
        console.log("------>All bids:"+ this.bids)
        this.bids = this.bids.filter((x) => { return x.item == String(this.item_id); });
        console.log("------>All bids on item:"+ this.bids)
        this.max_bid = Math.max(...this.bids.map(o => o.bid_amount),this.item.starting_price);
      },
      async getItem(){
        console.log("Bidding item id:"+this.item_id)
        let response = await fetch("/api/item/" +this.item_id);
        let data = await response.json();
        this.item = data;
      },
      async addBid(){
        console.log("Posting Bid")
        var current_date = new Date()
        var item_deadline = new Date(this.item.deadline)
        if(item_deadline>current_date){
            console.log("timing works")
        }
        let new_bid = (<HTMLInputElement>document.getElementById("inputBid")).value;
        let minimum_bid = parseFloat(this.item.starting_price)
        if (this.bids.length>0) minimum_bid = this.max_bid + 0.5
        console.log(new_bid)
        console.log(minimum_bid)
        if (parseFloat(new_bid) >= minimum_bid && item_deadline>current_date){
            let now = new Date();
            let new_entry = {
                bid_amount: new_bid,
                bid_time: now,
                item: this.item_id,
                user: this.user_id
            }
            console.log("The POST:" + JSON.stringify(new_entry))
            let response = await fetch("/api/bids/", {
                method: 'POST',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(new_entry)
            });
            if (response.ok) {
                this.getBids();
                (<HTMLInputElement>document.getElementById("inputBid")).value = ""
            }
        }
        else if (parseFloat(new_bid) < minimum_bid){
            alert("Please ad a minimum bid value of £" + (this.max_bid + 0.5));
        } else {
            alert("This biding is now closed");
        }
      },
    }
})
</script>

<style>
.card {
    padding: 1em;
    margin: 2em 0 1em 0em;
}
div.col{
    padding: 0;
}
.btn-primary {
    margin-top: 1rem;
}
#inputBid {
    width: 91%;
}
</style>