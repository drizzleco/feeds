export const dashPreview = {
    props: ['dashboard'],
    template: `<div class="dash-preview col s12 m6" @click="this.window.location='/dashboard/'+dashboard.slug">
                    <div class="card-panel cyan lighten-1 white-text">
                        <h4>{{dashboard.name}}</h4>
                        <span>Created on: {{new Date(dashboard.created).toLocaleString()}} </span>
                        <p>Feeds: {{feeds}} <span v-if="!feeds">none yet!</span></p>
                    </div>
                </div>`,
    computed: {
        feeds: function () {
            let feed_names = this.dashboard.feeds.map(feed => {
                return feed.name
            })
            return feed_names.join(", ")
        }
    }
};
