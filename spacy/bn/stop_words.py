# encoding: utf8
from __future__ import unicode_literals


STOP_WORDS = set("""
অতএব অথচ অথবা অনুযায়ী অনেক অনেকে অনেকেই অন্তত  অবধি অবশ্য অর্থাৎ অন্য অনুযায়ী অর্ধভাগে
আগামী আগে আগেই আছে আজ আদ্যভাগে আপনার আপনি আবার আমরা আমাকে আমাদের আমার  আমি আর আরও 
ইত্যাদি ইহা 
উচিত উনি উপর উপরে উত্তর
এ এঁদের এঁরা এই এক একই একজন একটা একটি  একবার একে এখন এখনও এখানে এখানেই এটা এসো
এটাই এটি এত এতটাই এতে এদের এবং এবার এমন এমনি এমনকি এর এরা এলো এস এসে 
ঐ 
ও ওঁদের ওঁর ওঁরা ওই ওকে ওখানে ওদের ওর ওরা 
কখনও কত কথা কবে কয়েক  কয়েকটি করছে করছেন করতে  করবে করবেন করলে কয়েক  কয়েকটি করিয়ে করিয়া করায়
করলেন করা করাই করায় করার করি করিতে করিয়া করিয়ে করে করেই করেছিলেন করেছে করেছেন করেন কাউকে 
কাছ কাছে কাজ কাজে কারও কারণ কি কিংবা কিছু কিছুই কিন্তু কী কে কেউ কেউই কেন কোন কোনও কোনো কেমনে কোটি
ক্ষেত্রে খুব 
গিয়ে গিয়েছে গুলি গেছে গেল গেলে গোটা গিয়ে গিয়েছে
চলে চান চায় চেয়ে চায় চেয়ে চার চালু চেষ্টা 
ছাড়া ছাড়াও ছিল ছিলেন ছাড়া ছাড়াও
জন জনকে জনের জন্য জন্যে জানতে জানা জানানো জানায়  জানিয়ে  জানিয়েছে জানায় জাানিয়ে জানিয়েছে
টি 
ঠিক 
তখন তত তথা তবু তবে তা তাঁকে তাঁদের তাঁর তাঁরা তাঁহারা তাই তাও তাকে তাতে তাদের তার তারপর তারা তারই তাহলে তাহা তাহাতে তাহার তিনই 
তিনি তিনিও তুমি তুলে তেমন তো তোমার 
থাকবে থাকবেন থাকা থাকায় থাকে থাকেন থেকে থেকেই  থেকেও থাকায়
দিকে দিতে দিয়ে দিয়েছে দিয়েছেন দিলেন দিয়ে দু  দুটি  দুটো দেওয়া দেওয়ার দেখতে দেখা দেখে দেন দেয়  দেশের  
দ্বারা দিয়েছে দিয়েছেন দেয় দেওয়া দেওয়ার দিন দুই
ধরা ধরে 
নয় না নাই নাকি নাগাদ নানা নিজে নিজেই নিজেদের নিজের নিতে নিয়ে নিয়ে নেই নেওয়া নেওয়ার নয় নতুন
পক্ষে পর পরে পরেই পরেও পর্যন্ত পাওয়া পারি পারে পারেন পেয়ে প্রতি প্রভৃতি প্রায় পাওয়া পেয়ে প্রায় পাঁচ প্রথম প্রাথমিক
ফলে ফিরে ফের 
বছর বদলে বরং বলতে বলল বললেন বলা বলে বলেছেন বলেন  বসে বহু বা বাদে বার বিনা বিভিন্ন বিশেষ বিষয়টি বেশ ব্যবহার ব্যাপারে বক্তব্য বন বেশি
ভাবে  ভাবেই 
মত মতো মতোই মধ্যভাগে মধ্যে মধ্যেই  মধ্যেও মনে মাত্র মাধ্যমে মানুষ মানুষের মোট মোটেই 
যখন যত যতটা যথেষ্ট যদি যদিও যা যাঁর যাঁরা যাওয়া  যাওয়ার যাকে যাচ্ছে যাতে যাদের যান যাবে যায় যার  যারা যায় যিনি যে যেখানে যেতে যেন 
যেমন 
রকম রয়েছে রাখা রেখে রয়েছে 
লক্ষ 
শুধু শুরু 
সাধারণ সামনে সঙ্গে সঙ্গেও সব সবার সমস্ত সম্প্রতি সময় সহ সহিত সাথে সুতরাং সে  সেই সেখান সেখানে  সেটা সেটাই সেটাও সেটি স্পষ্ট স্বয়ং 
হইতে হইবে হইয়া হওয়া হওয়ায় হওয়ার হচ্ছে হত হতে হতেই হন হবে হবেন হয় হয়তো হয়নি হয়ে হয়েই হয়েছিল হয়েছে হাজার
হয়েছেন হল হলে হলেই হলেও হলো হিসাবে হিসেবে হৈলে হোক হয় হয়ে হয়েছে হৈতে হইয়া  হয়েছিল হয়েছেন হয়নি হয়েই হয়তো হওয়া হওয়ার হওয়ায়
""".split())
