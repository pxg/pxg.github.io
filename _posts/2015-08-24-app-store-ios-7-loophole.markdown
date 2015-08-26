---
layout: post
title:  App Store iOS 7 loophole
description: Apple approval process doesn't find iOS 7 bug
date:   2015-08-24 12:09:00
categories: Swift Apple iPhone
---
When we first released [Warblr](https://itunes.apple.com/gb/app/warblr/id1013921979?ls=1&mt=8) we had a few angry customers complaining the app crashed as soon as they loaded it up. Of course we wanted to solve this problem as soon as possible, especially since Warlbr is a paid app.

From talking to the users with the issue we found many of them were using the iPhone 4. Users with newer iPhones experiencing the problem were using iOS 7. [Our research](https://en.wikipedia.org/wiki/List_of_iOS_devices#iPhone) confirmed the newest operating system the iPhone 4 can support is iOS 7.

We could advise the people with newer models to upgrade to iOS 8 but this wouldn't work for the iPhone 4 users. The confusing thing was the app had been approved by Apple App Store.

##Emulating iOS 7

The iPhone 4S is the oldest device you can emulate with Xcode 6.4, so this is what we'd tested the app with. Out of the box the iPhone 4S simulator runs with iOS 8.4. You can download an iOS 7.1 simulator by going into:

`XCode -> Preferences -> Downloads`

![Xcode preferences downloads](/assets/images/posts/xcode_downloads.png)
Now grab yourself a coffee, the download takes a while. Once it's done open up the iOS simulator.

`iOS Simulator -> Hardware -> Device -> Manage Devices`

![Xcode simulators](/assets/images/posts/xcode_simulators.png)
Click the plus icon in the bottom right hand corner of this screen to add a new simulated device running iOS 7. The new device will now appear in the list of devices that Xcode can run your app on.

![Xcoder run on](/assets/images/posts/xcode_run_on.png)

As far as I can tell you can only get emulators for older versions of iOS not older hardware such as the iPhone 4. Thankfully I was able to recreate the crashing bug with iOS 7, running on any device.

##Fixing iOS 7 crash

It turns out the technique to access the users location changed in iOS 8. Below is the fixed code.

{% highlight swift %}
override func viewDidLoad() {
    super.viewDidLoad()
    let Device = UIDevice.currentDevice()
    let iosVersion = NSString(string: Device.systemVersion).doubleValue

    locationManager.delegate = self
    if iosVersion >= 8 {
        locationManager.requestWhenInUseAuthorization()
    }
    locationManager.desiredAccuracy = kCLLocationAccuracyBest
    locationManager.startUpdatingLocation()
}
{% endhighlight %}

The above code is used in a view controller that implements `CLLocationManagerDelegate`.

##Conclusion
When building apps it's best to have physical versions of older Apple Devices running older versions of iOS.


I found it strange that Apple didn't catch the iOS 7 bug during the approval process. The Apple App Store review  process is notoriously slow and painful, Warblr was rejected twice before it was approved. However no problems with iOS were mentioned.

I can only conclude that Apple don't test the App on older devices or older versions of iOS. My theory is they don't particularly care about users on old versions of their operating systems and users who use older hardware.
