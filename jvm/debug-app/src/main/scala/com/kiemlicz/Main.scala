package com.kiemlicz

import scala.collection.mutable.ListBuffer

class Heavy(val unsafeStorage: ListBuffer[Array[Byte]]) {
  unsafeStorage.insert(0, new Array[Byte](1))
  def eat(chunk: Array[Byte]): Unit = {
    unsafeStorage += chunk
  }
  def bite(chunk: Array[Byte]): Unit = {
    unsafeStorage.update(0, chunk)
  }
}
object Main {
  val MB = 1048576
  def main(args: Array[String]): Unit = {
    val rt = Runtime.getRuntime
    val storage = new Heavy(new ListBuffer[Array[Byte]])
    println(s"Hi: ${rt.freeMemory()}")
    while (true) {
//      storage.eat(new Array[Byte](MB))
      storage.bite(new Array[Byte](MB))
      println(s"${rt.freeMemory()}")
    }
  }
}
