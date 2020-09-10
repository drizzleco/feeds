export const feedPreview = {
    props: ['feed'],
    template: `<div class = "feed-preview card-panel row teal accent-3 black-text" >
        <div class = "col m6 s12 d-flex-center">
            <h4 class="clickable" @click="this.window.location='/feed/'+feed.slug">{{feed.name}}</h4>
            <span v-if="feed.data.length">Last updated {{timeDiffFromNow(feed.data[0].created)}} ago</span>
        </div>
        <div class = "col m6 s12 d-flex-center">
            <h6>Last value:</h6>
            <span v-if="!feed.data.length">No data yet!</span>
            <div v-if="feed.data.length">
                <p v-if="feed.kind=='text'">{{feed.data[0].value}}</p>
                <h5 v-if="feed.kind=='number'">{{feed.data[0].value}}</h5>
                <img width="100%" :src="feed.data[0].value" v-if="feed.kind=='image'">
                <div v-if="feed.kind=='boolean'" :class="'bool-mark ' + feed.data[0].value"></div>
            </div>
        </div>
    </div>`,
    methods: {
        timeDiffFromNow
    }
};
